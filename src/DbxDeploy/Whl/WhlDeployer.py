from DbxDeploy.Setup.SetupBuilder import SetupBuilder
from DbxDeploy.Setup.SetupInterface import SetupInterface
from DbxDeploy.Whl.WhlUploader import WhlUploader
from DbxDeploy.Setup.PackageMetadata import PackageMetadata
from pathlib import Path
from logging import Logger

class WhlDeployer:

    def __init__(
        self,
        projectBasePath: str,
        logger: Logger,
        setupBuilder: SetupBuilder,
        whlUploader: WhlUploader
    ):
        self.__projectBasePath = Path(projectBasePath)
        self.__logger = logger
        self.__setupBuilder = setupBuilder
        self.__whlUploader = whlUploader

    def deploy(self, setup: SetupInterface, packageMetadata: PackageMetadata):
        self.__logger.info('Building app package (WHL)')

        self.__setupBuilder.build(setup, self.__projectBasePath)

        whlFileName = packageMetadata.getWhlFileName()

        whlFilePath = self.__projectBasePath.joinpath(Path('dist/' + whlFileName))

        with whlFilePath.open('rb') as file:
            content = file.read()
            self.__whlUploader.upload(content, whlFileName)
            self.__whlUploader.upload(content, packageMetadata.getCurrentWhlFileName())

        self.__logger.info('App package uploaded')
