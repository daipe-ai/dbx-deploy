from pathlib import Path
from DbxDeploy.Dbc.DbcCreator import DbcCreator
from DbxDeploy.Dbc.DbcUploader import DbcUploader
from DbxDeploy.Setup.PackageMetadata import PackageMetadata
from logging import Logger

class DbcDeployer:

    def __init__(
        self,
        projectBasePath: str,
        logger: Logger,
        dbcCreator: DbcCreator,
        dbcUploader: DbcUploader,
    ):
        self.__projectBasePath = Path(projectBasePath)
        self.__logger = logger
        self.__dbcCreator = dbcCreator
        self.__dbcUploader = dbcUploader

    def deploy(self, packageMetadata: PackageMetadata):
        self.__logger.info('Building notebooks into DBC package')

        notebookPaths = []

        for path in self.__projectBasePath.joinpath('src').glob('**/*.ipynb'):
            notebookPaths.append(path.relative_to(self.__projectBasePath))

        dbcContent = self.__dbcCreator.create(notebookPaths, self.__projectBasePath, packageMetadata)

        self.__dbcUploader.upload(dbcContent, packageMetadata.getVersion())

        self.__logger.info('DBC deployment finished')
