from argparse import Namespace
from logging import Logger
from pathlib import PurePosixPath, Path
from zipfile import ZipInfo, ZipFile
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.dbc.DbcNotebookConverter import DbcNotebookConverter
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException
from dbxdeploy.notebook.loader import load_notebook
from dbxdeploy.workspace.DbcFilesHandler import DbcFilesHandler
from dbxdeploy.workspace.WorkspaceExporter import WorkspaceExporter
from dbxdeploy.black.BlackChecker import BlackChecker


class WorkspaceExportCommand(ConsoleCommand):
    def __init__(
        self,
        workspace_base_dir: PurePosixPath,
        project_base_dir: Path,
        relative_base_dir: str,
        logger: Logger,
        notebook_converter: NotebookConverterInterface,
        workspace_exporter: WorkspaceExporter,
        dbc_files_handler: DbcFilesHandler,
        dbc_notebook_converter: DbcNotebookConverter,
        black_checker: BlackChecker,
    ):
        self.__workspace_base_dir = workspace_base_dir
        self.__local_base_dir = project_base_dir.joinpath(relative_base_dir)
        self.__logger = logger
        self.__notebook_converter = notebook_converter
        self.__workspace_exporter = workspace_exporter
        self.__dbc_files_handler = dbc_files_handler
        self.__dbc_notebook_converter = dbc_notebook_converter
        self.__black_checker = black_checker

    def get_command(self) -> str:
        return "dbx:workspace:export"

    def get_description(self):
        return "Export notebooks from Databricks workspace to local project"

    def run(self, input_args: Namespace):
        self.__logger.info(f"Exporting {self.__workspace_base_dir} to {self.__local_base_dir}")

        if self.__black_checker.is_black_enabled and not self.__black_checker.is_black_installed:
            self.__logger.warning("Black enabled, but not installed. Skipping black formatting.")

        dbc_content = self.__workspace_exporter.export(self.__workspace_base_dir)
        self.__dbc_files_handler.handle(dbc_content, self.__read_file)

        self.__logger.info("Export completed")

    def __read_file(self, zip_file: ZipFile, file: ZipInfo):
        if file.orig_filename[-1:] == "/":
            return

        file_path_without_rootdir = (
            file.orig_filename[file.orig_filename.index("/") + 1 : file.orig_filename.rindex(".")] + ".py"  # noqa: 5203
        )
        local_file_path = self.__local_base_dir.joinpath(file_path_without_rootdir)

        if local_file_path.exists():
            local_file_source = load_notebook(local_file_path)

            try:
                self.__notebook_converter.validate_source(local_file_source)
            except UnexpectedSourceException:
                self.__logger.error(f"Skipping unrecognized file {local_file_path}")
                return

        if self.__black_checker.is_black_enabled and self.__black_checker.is_black_installed:
            try:
                self.__dbc_notebook_converter.convert(zip_file, file)

            except Exception as ex:
                self.__logger.error(f"Black cannot format file {file.orig_filename}, skipping...")
                self.__logger.error(ex)
                return

        py_content = self.__dbc_notebook_converter.convert(zip_file, file)
        self.__write_py_content(local_file_path, py_content)

    def __write_py_content(self, local_file_path, py_content):
        if not local_file_path.parent.exists():
            local_file_path.parent.mkdir(parents=True)

        with local_file_path.open("wb") as f:
            f.write(py_content)
