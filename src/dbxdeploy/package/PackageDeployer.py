from dbxdeploy.package.PackageBuilder import PackageBuilder
from dbxdeploy.package.PackageMetadata import PackageMetadata
from pathlib import Path
from logging import Logger
from dbxdeploy.deploy.TargetPathsResolver import TargetPathsResolver
from dbxdeploy.deploy.LocalPathsResolver import LocalPathsResolver
from dbxdeploy.package.PackageUploaderInterface import PackageUploaderInterface

class PackageDeployer:

    def __init__(
        self,
        projectBaseDir: Path,
        offlineInstall: bool,
        logger: Logger,
        packageUploader: PackageUploaderInterface,
        packageBuilder: PackageBuilder,
        targetPathsResolver: TargetPathsResolver,
        localPathsResolver: LocalPathsResolver,
    ):
        self.__projectBaseDir = projectBaseDir
        self.__offlineInstall = offlineInstall
        self.__logger = logger
        self.__packageUploader = packageUploader
        self.__packageBuilder = packageBuilder
        self.__targetPathsResolver = targetPathsResolver
        self.__localPathsResolver = localPathsResolver

    def deploy(self, packageMetadata: PackageMetadata):
        def whlContentReadyCallback():
            if self.__offlineInstall:
                for dependency in packageMetadata.dependencies:
                    dependencyLocalPath = self.__localPathsResolver.getDependencyDistPath(dependency)
                    dependencyFilename = self.__localPathsResolver.getDependencyFilenameFromPath(dependencyLocalPath)
                    dependencyDeployPath = self.__targetPathsResolver.getDependencyUploadPathForDeploy(packageMetadata, dependencyFilename)

                    if not self.__packageUploader.exists(dependencyDeployPath):
                        self.__upload(dependencyLocalPath, dependencyDeployPath)
                    else:
                        self.__logger.debug(f'Package at {dependencyDeployPath} already exists. Skipping...')

            masterPackageLocalPath = self.__localPathsResolver.getPackageDistPath(packageMetadata)
            masterPackageDeployPath = self.__targetPathsResolver.getPackageUploadPathForDeploy(packageMetadata)

            self.__upload(masterPackageLocalPath, masterPackageDeployPath)

        self.__invoke(packageMetadata, whlContentReadyCallback)

    def release(self, packageMetadata: PackageMetadata):
        def whlContentReadyCallback():
            if self.__offlineInstall:
                for dependency in packageMetadata.dependencies:
                    dependencyLocalPath = self.__localPathsResolver.getDependencyDistPath(dependency)
                    dependencyFilename = self.__localPathsResolver.getDependencyFilenameFromPath(dependencyLocalPath)
                    dependencyReleasePath = self.__targetPathsResolver.getDependencyUploadPathForRelease(packageMetadata, dependencyFilename)

                    self.__upload(dependencyLocalPath, dependencyReleasePath)

            masterPackageLocalPath = self.__localPathsResolver.getPackageDistPath(packageMetadata)
            masterPackageReleasePath = self.__targetPathsResolver.getPackageUploadPathForRelease(packageMetadata)

            self.__upload(masterPackageLocalPath, masterPackageReleasePath)

        self.__invoke(packageMetadata, whlContentReadyCallback)

    def __invoke(self, packageMetadata: PackageMetadata, whlContentReadyCallback: callable):
        self.__logger.info('Building master package (WHL)')

        self.__packageBuilder.build(self.__projectBaseDir, packageMetadata)

        whlContentReadyCallback()

        self.__logger.info('App package uploaded')

    def __upload(self, localPath: Path, targetPath: str):
        self.__logger.info(f'Uploading WHL package to {targetPath}')

        with localPath.open('rb') as file:
            self.__packageUploader.upload(file.read(), targetPath, overwrite=True)
