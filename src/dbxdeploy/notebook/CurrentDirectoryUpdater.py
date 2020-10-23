# pylint: disable = too-many-instance-attributes
import re
from logging import Logger
from typing import List
from zipfile import ZipInfo, ZipFile
from databricks_api import DatabricksAPI
from pathlib import PurePosixPath
from pygit2 import GitError # pylint: disable = no-name-in-module
from dbxdeploy.git.CurrentBranchResolver import CurrentBranchResolver
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
        workspaceBaseDir: PurePosixPath,
        gitDevBranch: str,
        logger: Logger,
        dbxApi: DatabricksAPI,
        workspaceExporter: WorkspaceExporter,
        dbcFilesHandler: DbcFilesHandler,
        workspaceImporter: WorkspaceImporter,
        databricksNotebookConverter: DatabricksNotebookConverter,
        currentBranchResolver: CurrentBranchResolver,
    ):
        self.__workspaceBaseDir = workspaceBaseDir
        self.__gitDevBranch = gitDevBranch
        self.__logger = logger
        self.__dbxApi = dbxApi
        self.__workspaceExporter = workspaceExporter
        self.__dbcFilesHandler = dbcFilesHandler
        self.__workspaceImporter = workspaceImporter
        self.__databricksNotebookConverter = databricksNotebookConverter
        self.__currentBranchResolver = currentBranchResolver

    def update(self, notebooks: List[Notebook], currentReleasePath: PurePosixPath, packagePath: str):
        if self.__shouldRemoveMissingNotebooks():
            self.__removeMissingNotebooks(currentReleasePath, notebooks)

        self.__updateNotebooks(currentReleasePath, notebooks, packagePath)

    def __removeMissingNotebooks(self, currentReleasePath: PurePosixPath, notebooks: List[Notebook]):
        existingNotebooksFullPaths = self.__resolveExistingNotebooksPaths(currentReleasePath)

        existingNotebooks = set(map(lambda path: re.sub(r'\.python$', '', path), existingNotebooksFullPaths))
        newNotebooks = set(map(lambda notebook: str(notebook.databricksRelativePath), notebooks))

        for notebookToDelete in existingNotebooks - newNotebooks:
            fullNotebookPath = self.__workspaceBaseDir.joinpath(notebookToDelete)
            self.__logger.warning('Removing deleted/missing notebook {}'.format(fullNotebookPath))
            self.__dbxApi.workspace.delete(str(fullNotebookPath))

    def __updateNotebooks(self, currentReleasePath: PurePosixPath, notebooks: List[Notebook], packagePath: str):
        for notebook in notebooks:
            targetPath = currentReleasePath.joinpath(notebook.databricksRelativePath)
            source = loadNotebook(notebook.path)

            try:
                self.__databricksNotebookConverter.validateSource(source)
            except UnexpectedSourceException:
                self.__logger.debug(f'Skipping unrecognized file {notebook.relativePath}')
                continue

            script = self.__databricksNotebookConverter.toWorkspaceImportNotebook(source, packagePath)

            self.__logger.info('Updating {}'.format(targetPath))
            self.__workspaceImporter.overwriteScript(script, targetPath)

    def __shouldRemoveMissingNotebooks(self):
        try:
            currentGitBranch = self.__currentBranchResolver.resolve()
        except GitError:
            return False

        return currentGitBranch == self.__gitDevBranch

    def __resolveExistingNotebooksPaths(self, currentReleasePath: PurePosixPath):
        fileNames = []

        def resolveFilenames(zipFile: ZipFile, file: ZipInfo): # pylint: disable = unused-argument
            if file.orig_filename[-1:] == '/':
                return

            """
            _current/myproject/foo/bar.python -> myproject/foo/bar.python (dbx:release)
            mybranch/myproject/foo/bar.python -> myproject/foo/bar.python (dbx:deploy)
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
