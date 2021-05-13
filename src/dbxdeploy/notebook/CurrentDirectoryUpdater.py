import re
from logging import Logger
from typing import List
from zipfile import ZipInfo, ZipFile
from databricks_api import DatabricksAPI
from pathlib import PurePosixPath
from pygit2 import GitError
from dbxdeploy.git.CurrentBranchResolver import CurrentBranchResolver
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException
from dbxdeploy.notebook.loader import load_notebook
from dbxdeploy.workspace.DbcFilesHandler import DbcFilesHandler
from dbxdeploy.workspace.WorkspaceExportException import WorkspaceExportException
from dbxdeploy.workspace.WorkspaceImporter import WorkspaceImporter
from dbxdeploy.workspace.WorkspaceExporter import WorkspaceExporter
from dbxdeploy.notebook.Notebook import Notebook


class CurrentDirectoryUpdater:
    def __init__(
        self,
        workspace_base_dir: PurePosixPath,
        git_dev_branch: str,
        logger: Logger,
        dbx_api: DatabricksAPI,
        notebook_converter: NotebookConverterInterface,
        workspace_exporter: WorkspaceExporter,
        dbc_files_handler: DbcFilesHandler,
        workspace_importer: WorkspaceImporter,
        current_branch_resolver: CurrentBranchResolver,
    ):
        self.__workspace_base_dir = workspace_base_dir
        self.__git_dev_branch = git_dev_branch
        self.__logger = logger
        self.__dbx_api = dbx_api
        self.__notebook_converter = notebook_converter
        self.__workspace_exporter = workspace_exporter
        self.__dbc_files_handler = dbc_files_handler
        self.__workspace_importer = workspace_importer
        self.__current_branch_resolver = current_branch_resolver

    def update(self, notebooks: List[Notebook], current_release_path: PurePosixPath, package_path: str, dependencies_dir_path: str):
        if self.__should_remove_missing_notebooks():
            self.__remove_missing_notebooks(current_release_path, notebooks)

        self.__update_notebooks(current_release_path, notebooks, package_path, dependencies_dir_path)

    def update_only_master_package_notebook(
        self, notebook: Notebook, current_release_path: PurePosixPath, package_path: str, dependencies_dir_path: str
    ):
        self.__update_notebooks(current_release_path, [notebook], package_path, dependencies_dir_path)

    def __remove_missing_notebooks(self, current_release_path: PurePosixPath, notebooks: List[Notebook]):
        existing_notebooks_full_paths = self.__resolve_existing_notebooks_paths(current_release_path)

        existing_notebooks = set(map(lambda path: re.sub(r"\.python$", "", path), existing_notebooks_full_paths))
        new_notebooks = set(map(lambda notebook: str(notebook.databricks_relative_path), notebooks))

        for notebook_to_delete in existing_notebooks - new_notebooks:
            full_notebook_path = self.__workspace_base_dir.joinpath(notebook_to_delete)
            self.__logger.warning("Removing deleted/missing notebook {}".format(full_notebook_path))
            self.__dbx_api.workspace.delete(str(full_notebook_path))

    def __update_notebooks(
        self, current_release_path: PurePosixPath, notebooks: List[Notebook], package_path: str, dependencies_dir_path: str
    ):
        for notebook in notebooks:
            target_path = current_release_path.joinpath(notebook.databricks_relative_path)
            source = load_notebook(notebook.path)

            try:
                self.__notebook_converter.validate_source(source)
            except UnexpectedSourceException:
                self.__logger.debug(f"Skipping unrecognized file {notebook.relative_path}")
                continue

            script = self.__notebook_converter.to_workspace_import_notebook(source, package_path, dependencies_dir_path)

            self.__logger.info("Updating {}".format(target_path))
            self.__workspace_importer.overwrite_script(script, target_path)

    def __should_remove_missing_notebooks(self):
        try:
            current_git_branch = self.__current_branch_resolver.resolve()
        except GitError:
            return False

        return current_git_branch == self.__git_dev_branch

    def __resolve_existing_notebooks_paths(self, current_release_path: PurePosixPath):
        file_names = []

        def resolve_filenames(zip_file: ZipFile, file: ZipInfo):
            if file.orig_filename[-1:] == "/":
                return

            """
            _current/myproject/foo/bar.python -> myproject/foo/bar.python (dbx:release)
            mybranch/myproject/foo/bar.python -> myproject/foo/bar.python (dbx:deploy)
            """
            file_path_without_rootdir = file.orig_filename[file.orig_filename.index("/") + 1 :]  # noqa: 5203

            file_names.append(file_path_without_rootdir)

        try:
            dbc_content = self.__workspace_exporter.export(current_release_path)
        except WorkspaceExportException:
            self.__logger.error("Unable to compare new notebooks to the existing ones in workspace")
            return []

        self.__dbc_files_handler.handle(dbc_content, resolve_filenames)

        return file_names
