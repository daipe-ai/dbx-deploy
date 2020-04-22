from dbxdeploy.deploy.CurrentAndReleaseDeployer import CurrentAndReleaseDeployer
from dbxdeploy.package.PackageMetadataLoader import PackageMetadataLoader
from dbxdeploy.package.PackageDeployer import PackageDeployer
from pathlib import Path
import asyncio

class Deployer:

    def __init__(
        self,
        projectBaseDir: Path,
        packageMetadataLoader: PackageMetadataLoader,
        currentAndReleaseDeployer: CurrentAndReleaseDeployer,
        packageDeployer: PackageDeployer,
    ):
        self.__projectBaseDir = projectBaseDir
        self.__packageMetadataLoader = packageMetadataLoader
        self.__currentAndReleaseDeployer = currentAndReleaseDeployer
        self.__packageDeployer = packageDeployer

    async def deploy(self):
        packageMetadata = self.__packageMetadataLoader.load(self.__projectBaseDir)

        loop = asyncio.get_event_loop()

        packageDeployFuture = loop.run_in_executor(None, self.__packageDeployer.deploy, packageMetadata)
        dbcDeployFuture = loop.run_in_executor(None, self.__currentAndReleaseDeployer.deploy, packageMetadata)

        await packageDeployFuture
        await dbcDeployFuture
