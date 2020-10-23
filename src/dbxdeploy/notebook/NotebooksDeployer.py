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

class NotebooksDeployer:

    def __init__(
        self,
        workspaceBaseDir: PurePosixPath,
        packageBaseDir: str,
        logger: Logger,
        dbxApi: DatabricksAPI,
        dbcCreator: DbcCreator,
        dbcUploader: DbcUploader,
        currentDirectoryUpdater: CurrentDirectoryUpdater,
    ):
        self.__workspaceBaseDir = workspaceBaseDir
        self.__packageBaseDir = packageBaseDir
        self.__logger = logger
        self.__dbxApi = dbxApi
        self.__dbcCreator = dbcCreator
        self.__dbcUploader = dbcUploader
        self.__currentDirectoryUpdater = currentDirectoryUpdater

    def deploy(self, packageMetadata: PackageMetadata, notebooks: List[Notebook]):
        packagePath = packageMetadata.getPackageUploadPathForRelease(self.__packageBaseDir)

        self.__logger.info('All packages released, updating {}'.format(self.__workspaceBaseDir))
        self.__currentDirectoryUpdater.update(notebooks, self.__workspaceBaseDir, packagePath)

    def release(self, packageMetadata: PackageMetadata, notebooks: List[Notebook]):
        self.__logger.info('Building notebooks package (DBC)')
        dbcContent = self.__dbcCreator.create(notebooks, packageMetadata.getPackageUploadPathForRelease(self.__packageBaseDir))

        _currentPath = self.__workspaceBaseDir.joinpath('_current') # pylint: disable = invalid-name
        releasePath = packageMetadata.getWorkspaceReleasePath(self.__workspaceBaseDir)

        self.__logger.info('Uploading notebooks package to {}'.format(releasePath))
        self.__dbcUploader.upload(dbcContent, releasePath)

        self.__logger.info('Cleaning up {} if exists'.format(_currentPath))

        try:
            self.__dbxApi.workspace.delete(str(_currentPath), recursive=True)
        except HTTPError as e:
            if e.response.status_code != 404:
                raise

        self.__logger.info('Uploading notebooks package to {}'.format(_currentPath))
        self.__dbcUploader.upload(dbcContent, _currentPath)
