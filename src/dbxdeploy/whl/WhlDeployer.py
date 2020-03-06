from dbxdeploy.whl.WhlBuilder import WhlBuilder
from dbxdeploy.whl.WhlUploader import WhlUploader
from dbxdeploy.package.PackageMetadata import PackageMetadata
from pathlib import Path, PurePosixPath
from logging import Logger

class WhlDeployer:

    def __init__(
        self,
        projectBasePath: Path,
        dbfsBasePath: str,
        logger: Logger,
        whlBuilder: WhlBuilder,
        whlUploader: WhlUploader
    ):
        self.__projectBasePath = projectBasePath
        self.__dbfsBasePath = PurePosixPath(dbfsBasePath)
        self.__logger = logger
        self.__whlBuilder = whlBuilder
        self.__whlUploader = whlUploader

    def deploy(self, packageMetadata: PackageMetadata):
        self.__logger.info('Building app package (WHL)')

        self.__whlBuilder.build(self.__projectBasePath)

        whlFilePath = self.__projectBasePath.joinpath(Path('dist')).joinpath(packageMetadata.getWhlFileName())

        with whlFilePath.open('rb') as file:
            content = file.read()
            self.__whlUploader.upload(content, packageMetadata.getWhlUploadPathForRelease(self.__dbfsBasePath))
            self.__whlUploader.upload(content, packageMetadata.getWhlUploadPathForCurrent(self.__dbfsBasePath))

        self.__logger.info('App package uploaded')
