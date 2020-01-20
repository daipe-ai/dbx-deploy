from dbxdeploy.package.PackageMetadataLoader import PackageMetadataLoader
from dbxdeploy.whl.WhlDeployer import WhlDeployer
from dbxdeploy.notebook.NotebooksDeployer import NotebooksDeployer
from pathlib import Path
import asyncio

class Deployer:

    def __init__(
        self,
        projectBasePath: Path,
        packageMetadataLoader: PackageMetadataLoader,
        notebooksDeployer: NotebooksDeployer,
        whlDeployer: WhlDeployer,
    ):
        self.__projectBasePath = projectBasePath
        self.__packageMetadataLoader = packageMetadataLoader
        self.__notebooksDeployer = notebooksDeployer
        self.__whlDeployer = whlDeployer

    async def deploy(self):
        packageMetadata = self.__packageMetadataLoader.load(self.__projectBasePath)

        loop = asyncio.get_event_loop()

        whlDeployFuture = loop.run_in_executor(None, self.__whlDeployer.deploy, packageMetadata)
        dbcDeployFuture = loop.run_in_executor(None, self.__notebooksDeployer.deployWithCurrent, packageMetadata)

        await whlDeployFuture
        await dbcDeployFuture
