from pathlib import PurePosixPath
from DbxDeploy.Dbc.DbcCreator import DbcCreator
from DbxDeploy.Dbc.DbcUploader import DbcUploader
from DbxDeploy.Notebook.CurrentDirectoryUpdater import CurrentDirectoryUpdater
from DbxDeploy.Notebook.NotebooksLocator import NotebooksLocator
from DbxDeploy.Package.PackageMetadata import PackageMetadata
from logging import Logger

class NotebooksDeployer:

    def __init__(
        self,
        dbxProjectRoot: str,
        whlBaseDir: str,
        logger: Logger,
        dbcCreator: DbcCreator,
        dbcUploader: DbcUploader,
        currentDirectoryUpdater: CurrentDirectoryUpdater,
        notebooksLocator: NotebooksLocator,
    ):
        self.__dbxProjectRoot = PurePosixPath(dbxProjectRoot)
        self.__whlBaseDir = PurePosixPath(whlBaseDir)
        self.__logger = logger
        self.__dbcCreator = dbcCreator
        self.__dbcUploader = dbcUploader
        self.__currentDirectoryUpdater = currentDirectoryUpdater
        self.__notebooksLocator = notebooksLocator

    def deploy(self, packageMetadata: PackageMetadata):
        notebooks = self.__notebooksLocator.locate()
        self.__logger.info('Building notebooks package (DBC)')
        dbcContent = self.__dbcCreator.create(notebooks, packageMetadata.getWhlUploadPathForRelease(self.__whlBaseDir))

        releasePath = packageMetadata.getWorkspaceReleasePath(self.__dbxProjectRoot)
        self.__logger.info('Uploading notebooks package to {}'.format(releasePath))
        self.__dbcUploader.upload(dbcContent, releasePath)

        return notebooks

    def deployWithCurrent(self, packageMetadata: PackageMetadata):
        notebooks = self.deploy(packageMetadata)

        currentReleasePath = self.__dbxProjectRoot.joinpath('_current')
        whlFilePath = packageMetadata.getWhlUploadPathForRelease(self.__whlBaseDir)

        self.__logger.info('All packages released, updating {}'.format(currentReleasePath))
        self.__currentDirectoryUpdater.update(notebooks, currentReleasePath, whlFilePath)
