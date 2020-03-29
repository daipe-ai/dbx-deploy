from logging import Logger
from typing import List
from databricks_api import DatabricksAPI
from pathlib import PurePosixPath
from dbxdeploy.notebook.ConverterResolver import ConverterResolver
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException
from dbxdeploy.workspace.WorkspaceImporter import WorkspaceImporter
from dbxdeploy.workspace.PathNotExistException import PathNotExistException
from dbxdeploy.workspace.WorkspaceExporter import WorkspaceExporter
from dbxdeploy.notebook.Notebook import Notebook
import re

class CurrentDirectoryUpdater:

    def __init__(
        self,
        dbxProjectRoot: PurePosixPath,
        logger: Logger,
        dbxApi: DatabricksAPI,
        workspaceExporter: WorkspaceExporter,
        workspaceImporter: WorkspaceImporter,
        converterResolver: ConverterResolver,
    ):
        self.__dbxProjectRoot = dbxProjectRoot
        self.__logger = logger
        self.__dbxApi = dbxApi
        self.__workspaceExporter = workspaceExporter
        self.__workspaceImporter = workspaceImporter
        self.__converterResolver = converterResolver

    def update(self, notebooks: List[Notebook], currentReleasePath: PurePosixPath, whlFilePath: PurePosixPath):
        self.__removeDeletedNotebooks(currentReleasePath, notebooks)
        self.__updateNotebooks(currentReleasePath, notebooks, whlFilePath)

    def __removeDeletedNotebooks(self, currentReleasePath: PurePosixPath, notebooks: List[Notebook]):
        try:
            existingNotebooksFullPaths = self.__workspaceExporter.export(currentReleasePath)
        except PathNotExistException:
            existingNotebooksFullPaths = []

        existingNotebooks = set(map(lambda path: re.sub(r'\.python$', '', path), existingNotebooksFullPaths))
        newNotebooks = set(map(lambda notebook: str(notebook.databricksRelativePath), notebooks))

        for notebookToDelete in existingNotebooks - newNotebooks:
            fullNotebookPath = self.__dbxProjectRoot.joinpath(notebookToDelete)
            self.__logger.warning('Removing deleted notebook {}'.format(fullNotebookPath))
            self.__dbxApi.workspace.delete(str(fullNotebookPath))

    def __updateNotebooks(self, currentReleasePath: PurePosixPath, notebooks: List[Notebook], whlFilePath: PurePosixPath):
        for notebook in notebooks:
            targetPath = currentReleasePath.joinpath(notebook.databricksRelativePath)
            converter = self.__converterResolver.resolve(notebook.converterClass)

            try:
                source = converter.loadSource(notebook.path)
            except UnexpectedSourceException:
                continue

            script = converter.toWorkspaceImportNotebook(source, whlFilePath)

            self.__logger.info('Updating {}'.format(targetPath))
            self.__workspaceImporter.overwriteScript(script, targetPath)
