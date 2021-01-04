from dbxdeploy.package.PackageBuilder import PackageBuilder
from dbxdeploy.package.PackageMetadata import PackageMetadata
from pathlib import Path
from logging import Logger
from dbxdeploy.deploy.TargetPathsResolver import TargetPathsResolver
from dbxdeploy.package.PackageUploaderInterface import PackageUploaderInterface

class PackageDeployer:

    def __init__(
        self,
        projectBaseDir: Path,
        logger: Logger,
        packageUploader: PackageUploaderInterface,
        packageBuilder: PackageBuilder,
        targetPathsResolver: TargetPathsResolver,
    ):
        self.__projectBaseDir = projectBaseDir
        self.__logger = logger
        self.__packageUploader = packageUploader
        self.__packageBuilder = packageBuilder
        self.__targetPathsResolver = targetPathsResolver

    def deploy(self, packageMetadata: PackageMetadata):
        self.__logger.info('Building master package (WHL)')

        packagePath = self.__packageBuilder.build(self.__projectBaseDir, packageMetadata.getPackageFilename())

        with packagePath.open('rb') as file:
            content = file.read()

            whlReleasePath = self.__targetPathsResolver.getPackageUploadPathForRelease(packageMetadata)
            self.__logger.info(f'Uploading WHL package to {whlReleasePath}')
            self.__packageUploader.upload(content, whlReleasePath, overwrite=True)

            if self.__targetPathsResolver.hasPackageUploadPathForCurrent():
                whlCurrentPath = self.__targetPathsResolver.getPackageUploadPathForCurrent(packageMetadata)
                self.__logger.info(f'Uploading WHL package to {whlCurrentPath}')
                self.__packageUploader.upload(content, whlCurrentPath, overwrite=True)

        self.__logger.info('App package uploaded')
