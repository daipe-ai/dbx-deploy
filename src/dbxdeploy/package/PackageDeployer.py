from dbxdeploy.package.PackageBuilder import PackageBuilder
from dbxdeploy.package.PackageMetadata import PackageMetadata
from pathlib import Path
from logging import Logger
from dbxdeploy.package.PackageUploaderInterface import PackageUploaderInterface

class PackageDeployer:

    def __init__(
        self,
        projectBaseDir: Path,
        targetBasePath: str,
        logger: Logger,
        packageUploader: PackageUploaderInterface,
        packageBuilder: PackageBuilder,
    ):
        self.__projectBaseDir = projectBaseDir
        self.__targetBasePath = targetBasePath
        self.__logger = logger
        self.__packageUploader = packageUploader
        self.__packageBuilder = packageBuilder

    def deploy(self, packageMetadata: PackageMetadata):
        self.__logger.info('Building master package (WHL)')

        self.__packageBuilder.build(self.__projectBaseDir)

        packagePath = self.__projectBaseDir.joinpath(Path('dist')).joinpath(packageMetadata.getPackageFilename())

        with packagePath.open('rb') as file:
            content = file.read()

            whlReleasePath = packageMetadata.getPackageUploadPathForRelease(self.__targetBasePath)
            self.__logger.info(f'Uploading WHL package to {whlReleasePath}')
            self.__packageUploader.upload(content, whlReleasePath, overwrite=True)

            whlCurrentPath = packageMetadata.getPackageUploadPathForCurrent(self.__targetBasePath)
            self.__logger.info(f'Uploading WHL package to {whlCurrentPath}')
            self.__packageUploader.upload(content, whlCurrentPath, overwrite=True)

        self.__logger.info('App package uploaded')
