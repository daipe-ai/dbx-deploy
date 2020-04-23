from argparse import Namespace
from logging import Logger
from pathlib import PurePosixPath, Path
from zipfile import ZipInfo, ZipFile
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.dbc.DbcNotebookConverter import DbcNotebookConverter
from dbxdeploy.notebook.converter.DatabricksNotebookConverter import DatabricksNotebookConverter
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException
from dbxdeploy.notebook.loader import loadNotebook
from dbxdeploy.workspace.DbcFilesHandler import DbcFilesHandler
from dbxdeploy.workspace.WorkspaceExporter import WorkspaceExporter

class WorkspaceExportCommand(ConsoleCommand):

    def __init__(
        self,
        workspaceBaseDir: PurePosixPath,
        projectBaseDir: Path,
        relativeBaseDir: str,
        logger: Logger,
        workspaceExporter: WorkspaceExporter,
        dbcFilesHandler: DbcFilesHandler,
        databricksNotebookConverter: DatabricksNotebookConverter,
        dbcNotebookConverter: DbcNotebookConverter,
    ):
        self.__workspaceBaseDir = workspaceBaseDir
        self.__localBaseDir = projectBaseDir.joinpath(relativeBaseDir)
        self.__logger = logger
        self.__workspaceExporter = workspaceExporter
        self.__dbcFilesHandler = dbcFilesHandler
        self.__databricksNotebookConverter = databricksNotebookConverter
        self.__dbcNotebookConverter = dbcNotebookConverter

    def getCommand(self) -> str:
        return 'dbx:workspace:export'

    def getDescription(self):
        return 'Export notebooks from Databricks workspace to local project'

    def run(self, inputArgs: Namespace):
        self.__logger.info(f'Exporting {self.__workspaceBaseDir} to {self.__localBaseDir}')

        dbcContent = self.__workspaceExporter.export(self.__workspaceBaseDir)
        self.__dbcFilesHandler.handle(dbcContent, self.__readFile)

        self.__logger.info(f'Export completed')

    def __readFile(self, zipFile: ZipFile, file: ZipInfo):
        if file.orig_filename[-1:] == '/':
            return

        filePathWithoutRootdir = file.orig_filename[file.orig_filename.index('/') + 1:file.orig_filename.rindex('.')] + '.py'
        localFilePath = self.__localBaseDir.joinpath(filePathWithoutRootdir)

        if localFilePath.exists():
            localFileSource = loadNotebook(localFilePath)

            try:
                self.__databricksNotebookConverter.validateSource(localFileSource)
            except UnexpectedSourceException:
                self.__logger.error(f'Skipping unrecognized file {localFilePath}')
                return

        if not localFilePath.parent.exists():
            localFilePath.parent.mkdir(parents=True)

        with localFilePath.open('wb') as f:
            pyContent = self.__dbcNotebookConverter.convert(zipFile, file)
            f.write(pyContent)
