# pylint: disable = too-many-instance-attributes
import re
from logging import Logger
from typing import List
from zipfile import ZipInfo, ZipFile
from databricks_api import DatabricksAPI
from pathlib import PurePosixPath
from pygit2 import Repository, GitError # pylint: disable = no-name-in-module
from dbxdeploy.notebook.converter.DatabricksNotebookConverter import DatabricksNotebookConverter
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException
from dbxdeploy.notebook.loader import loadNotebook
from dbxdeploy.workspace.DbcFilesHandler import DbcFilesHandler
from dbxdeploy.workspace.WorkspaceExportException import WorkspaceExportException
from dbxdeploy.workspace.WorkspaceImporter import WorkspaceImporter
from dbxdeploy.workspace.WorkspaceExporter import WorkspaceExporter
from dbxdeploy.notebook.Notebook import Notebook

class CurrentDirectoryUpdater:

    def __init__(
        self,
        dbxProjectRoot: PurePosixPath,
        logger: Logger,
        dbxApi: DatabricksAPI,
        workspaceExporter: WorkspaceExporter,
        dbcFilesHandler: DbcFilesHandler,
        workspaceImporter: WorkspaceImporter,
        databricksNotebookConverter: DatabricksNotebookConverter,
    ):
        self.__dbxProjectRoot = dbxProjectRoot
        self.__logger = logger
        self.__dbxApi = dbxApi
        self.__workspaceExporter = workspaceExporter
        self.__dbcFilesHandler = dbcFilesHandler
        self.__workspaceImporter = workspaceImporter
        self.__databricksNotebookConverter = databricksNotebookConverter

    def update(self, notebooks: List[Notebook], currentReleasePath: PurePosixPath, whlFilePath: PurePosixPath):
        if self.__shouldRemoveMissingNotebooks():
            self.__removeMissingNotebooks(currentReleasePath, notebooks)

        self.__updateNotebooks(currentReleasePath, notebooks, whlFilePath)

    def __removeMissingNotebooks(self, currentReleasePath: PurePosixPath, notebooks: List[Notebook]):
        existingNotebooksFullPaths = self.__resolveExistingNotebooksPaths(currentReleasePath)

        existingNotebooks = set(map(lambda path: re.sub(r'\.python$', '', path), existingNotebooksFullPaths))
        newNotebooks = set(map(lambda notebook: str(notebook.databricksRelativePath), notebooks))

        for notebookToDelete in existingNotebooks - newNotebooks:
            fullNotebookPath = self.__dbxProjectRoot.joinpath(notebookToDelete)
            self.__logger.warning('Removing deleted/missing notebook {}'.format(fullNotebookPath))
            self.__dbxApi.workspace.delete(str(fullNotebookPath))

    def __updateNotebooks(self, currentReleasePath: PurePosixPath, notebooks: List[Notebook], whlFilePath: PurePosixPath):
        for notebook in notebooks:
            targetPath = currentReleasePath.joinpath(notebook.databricksRelativePath)
            source = loadNotebook(notebook.path)

            try:
                self.__databricksNotebookConverter.validateSource(source)
            except UnexpectedSourceException:
                self.__logger.debug(f'Skipping unrecognized file {notebook.relativePath}')
                continue

            script = self.__databricksNotebookConverter.toWorkspaceImportNotebook(source, whlFilePath)

            self.__logger.info('Updating {}'.format(targetPath))
            self.__workspaceImporter.overwriteScript(script, targetPath)

    def __shouldRemoveMissingNotebooks(self):
        try:
            currentGitBranch = Repository('.').head.shorthand
        except GitError:
            return False

        return currentGitBranch == 'master'

    def __resolveExistingNotebooksPaths(self, currentReleasePath: PurePosixPath):
        fileNames = []

        def resolveFilenames(zipFile: ZipFile, file: ZipInfo): # pylint: disable = unused-argument
            if file.orig_filename[-1:] == '/':
                return

            """
            _current/myproject/foo/bar.python -> myproject/foo/bar.python (releases enabled)
            mybranch/myproject/foo/bar.python -> myproject/foo/bar.python (releases disabled)
            """
            filePathWithoutRootdir = file.orig_filename[file.orig_filename.index('/') + 1:]

            fileNames.append(filePathWithoutRootdir)

        try:
            dbcContent = self.__workspaceExporter.export(currentReleasePath)
        except WorkspaceExportException:
            self.__logger.error('Unable to compare new notebooks to the existing ones in workspace')
            return []

        self.__dbcFilesHandler.handle(dbcContent, resolveFilenames)

        return fileNames
