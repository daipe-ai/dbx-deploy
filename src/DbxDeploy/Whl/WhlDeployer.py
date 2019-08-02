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
        self.__logger.info('Building WHL package')

        self.__setupBuilder.build(setup, self.__projectBasePath)

        whlFileName = packageMetadata.getWhlFileName()

        self.__logger.info('Uploading WHL package')

        whlFilePath = self.__projectBasePath.joinpath(Path('dist/' + whlFileName))

        with whlFilePath.open('rb') as file:
            self.__whlUploader.upload(file.read(), whlFileName)

        self.__logger.info('WHL package uploaded')
