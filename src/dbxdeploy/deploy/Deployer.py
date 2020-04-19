from dbxdeploy.deploy.CurrentAndReleaseDeployer import CurrentAndReleaseDeployer
from dbxdeploy.package.PackageMetadataLoader import PackageMetadataLoader
from dbxdeploy.whl.WhlDeployer import WhlDeployer
from pathlib import Path
import asyncio

class Deployer:

    def __init__(
        self,
        projectBaseDir: Path,
        packageMetadataLoader: PackageMetadataLoader,
        currentAndReleaseDeployer: CurrentAndReleaseDeployer,
        whlDeployer: WhlDeployer,
    ):
        self.__projectBaseDir = projectBaseDir
        self.__packageMetadataLoader = packageMetadataLoader
        self.__currentAndReleaseDeployer = currentAndReleaseDeployer
        self.__whlDeployer = whlDeployer

    async def deploy(self):
        packageMetadata = self.__packageMetadataLoader.load(self.__projectBaseDir)

        loop = asyncio.get_event_loop()

        whlDeployFuture = loop.run_in_executor(None, self.__whlDeployer.deploy, packageMetadata)
        dbcDeployFuture = loop.run_in_executor(None, self.__currentAndReleaseDeployer.deploy, packageMetadata)

        await whlDeployFuture
        await dbcDeployFuture
