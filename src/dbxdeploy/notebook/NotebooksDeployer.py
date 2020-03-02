from pathlib import PurePosixPath
from typing import List
from dbxdeploy.dbc.DbcCreator import DbcCreator
from dbxdeploy.dbc.DbcUploader import DbcUploader
from dbxdeploy.notebook.CurrentDirectoryUpdater import CurrentDirectoryUpdater
from dbxdeploy.notebook.Notebook import Notebook
from dbxdeploy.package.PackageMetadata import PackageMetadata
from logging import Logger

class NotebooksDeployer:

    def __init__(
        self,
        dbxProjectRoot: PurePosixPath,
        whlBaseDir: str,
        logger: Logger,
        dbcCreator: DbcCreator,
        dbcUploader: DbcUploader,
        currentDirectoryUpdater: CurrentDirectoryUpdater,
    ):
        self.__dbxProjectRoot = dbxProjectRoot
        self.__whlBaseDir = PurePosixPath(whlBaseDir)
        self.__logger = logger
        self.__dbcCreator = dbcCreator
        self.__dbcUploader = dbcUploader
        self.__currentDirectoryUpdater = currentDirectoryUpdater

    def deployRoot(self, packageMetadata: PackageMetadata, notebooks: List[Notebook]):
        whlFilePath = packageMetadata.getWhlUploadPathForRelease(self.__whlBaseDir)

        self.__logger.info('All packages released, updating {}'.format(self.__dbxProjectRoot))
        self.__currentDirectoryUpdater.update(notebooks, self.__dbxProjectRoot, whlFilePath)

    def deployRelease(self, packageMetadata: PackageMetadata, notebooks: List[Notebook]):
        self.__logger.info('Building notebooks package (DBC)')
        dbcContent = self.__dbcCreator.create(notebooks, packageMetadata.getWhlUploadPathForRelease(self.__whlBaseDir))

        releasePath = packageMetadata.getWorkspaceReleasePath(self.__dbxProjectRoot)
        self.__logger.info('Uploading notebooks package to {}'.format(releasePath))
        self.__dbcUploader.upload(dbcContent, releasePath)

    def deployCurrent(self, packageMetadata: PackageMetadata, notebooks: List[Notebook]):
        currentReleasePath = self.__dbxProjectRoot.joinpath('_current')
        whlFilePath = packageMetadata.getWhlUploadPathForRelease(self.__whlBaseDir)

        self.__logger.info('All packages released, updating {}'.format(currentReleasePath))
        self.__currentDirectoryUpdater.update(notebooks, currentReleasePath, whlFilePath)
