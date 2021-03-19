from pathlib import PurePosixPath
from typing import List
from requests.exceptions import HTTPError
from databricks_api import DatabricksAPI
from dbxdeploy.dbc.DbcCreator import DbcCreator
from dbxdeploy.dbc.DbcUploader import DbcUploader
from dbxdeploy.notebook.CurrentDirectoryUpdater import CurrentDirectoryUpdater
from dbxdeploy.notebook.Notebook import Notebook
from dbxdeploy.package.PackageMetadata import PackageMetadata
from logging import Logger
from dbxdeploy.deploy.TargetPathsResolver import TargetPathsResolver


class NotebooksDeployer:
    def __init__(
        self,
        workspace_base_dir: PurePosixPath,
        logger: Logger,
        dbx_api: DatabricksAPI,
        dbc_creator: DbcCreator,
        dbc_uploader: DbcUploader,
        current_directory_updater: CurrentDirectoryUpdater,
        target_paths_resolver: TargetPathsResolver,
    ):
        self.__workspace_base_dir = workspace_base_dir
        self.__logger = logger
        self.__dbx_api = dbx_api
        self.__dbc_creator = dbc_creator
        self.__dbc_uploader = dbc_uploader
        self.__current_directory_updater = current_directory_updater
        self.__target_paths_resolver = target_paths_resolver

    def deploy(self, package_metadata: PackageMetadata, notebooks: List[Notebook]):
        package_path = self.__target_paths_resolver.get_package_upload_path_for_deploy(package_metadata)
        dependencies_dir = self.__target_paths_resolver.get_dependencies_upload_dir_for_deploy(package_metadata)

        self.__logger.info(f"All packages released, updating {self.__workspace_base_dir}")
        self.__current_directory_updater.update(notebooks, self.__workspace_base_dir, package_path, dependencies_dir)

    def deploy_only_master_package_notebook(self, package_metadata: PackageMetadata, notebook: Notebook):
        package_path = self.__target_paths_resolver.get_package_upload_path_for_deploy(package_metadata)
        dependencies_dir = self.__target_paths_resolver.get_dependencies_upload_dir_for_deploy(package_metadata)

        self.__logger.info(f"All packages released, updating {self.__workspace_base_dir}")
        self.__current_directory_updater.update_only_master_package_notebook(
            notebook, self.__workspace_base_dir, package_path, dependencies_dir
        )

    def release(self, package_metadata: PackageMetadata, notebooks: List[Notebook]):
        package_path = self.__target_paths_resolver.get_package_upload_path_for_release(package_metadata)
        dependencies_dir = self.__target_paths_resolver.get_dependencies_upload_dir_for_release(package_metadata)

        self.__logger.info("Building notebooks package (DBC)")
        dbc_content = self.__dbc_creator.create(notebooks, package_path, dependencies_dir)

        _current_path = self.__target_paths_resolver.get_workspace_current_path(package_metadata)
        release_path = self.__target_paths_resolver.get_workspace_release_path(package_metadata)

        self.__logger.info(f"Uploading notebooks package to {release_path}")
        self.__dbc_uploader.upload(dbc_content, release_path)

        self.__logger.info(f"Cleaning up {_current_path} if exists")

        try:
            self.__dbx_api.workspace.delete(str(_current_path), recursive=True)
        except HTTPError as e:
            if e.response.status_code != 404:
                raise

        self.__logger.info(f"Uploading notebooks package to {_current_path}")
        self.__dbc_uploader.upload(dbc_content, _current_path)
