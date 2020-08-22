from dbxdeploy.dbfs.DbfsFileUploader import DbfsFileUploader
from dbxdeploy.package.PackageBuilder import PackageBuilder
from dbxdeploy.package.PackageMetadata import PackageMetadata
from pathlib import Path, PurePosixPath
from logging import Logger

class PackageDeployer:

    def __init__(
        self,
        projectBaseDir: Path,
        dbfsBasePath: str,
        logger: Logger,
        packageBuilder: PackageBuilder,
        packageUploader: DbfsFileUploader
    ):
        self.__projectBaseDir = projectBaseDir
        self.__dbfsBasePath = PurePosixPath(dbfsBasePath)
        self.__logger = logger
        self.__packageBuilder = packageBuilder
        self.__packageUploader = packageUploader

    def deploy(self, packageMetadata: PackageMetadata):
        self.__logger.info('Building master package (WHL)')

        self.__packageBuilder.build(self.__projectBaseDir)

        packagePath = self.__projectBaseDir.joinpath(Path('dist')).joinpath(packageMetadata.getPackageFilename())

        with packagePath.open('rb') as file:
            content = file.read()

            whlReleasePath = packageMetadata.getPackageUploadPathForRelease(self.__dbfsBasePath)
            self.__logger.info(f'Uploading WHL package to {whlReleasePath}')
            self.__packageUploader.upload(content, whlReleasePath, overwrite=True)

            whlCurrentPath = packageMetadata.getPackageUploadPathForCurrent(self.__dbfsBasePath)
            self.__logger.info(f'Uploading WHL package to {whlCurrentPath}')
            self.__packageUploader.upload(content, whlCurrentPath, overwrite=True)

        self.__logger.info('App package uploaded')
