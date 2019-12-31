from DbxDeploy.Package.PackageMetadataLoader import PackageMetadataLoader
from DbxDeploy.Whl.WhlDeployer import WhlDeployer
from DbxDeploy.Notebook.NotebooksDeployer import NotebooksDeployer
from pathlib import Path
import asyncio

class Deployer:

    def __init__(
        self,
        projectBasePath: str,
        packageMetadataLoader: PackageMetadataLoader,
        notebooksDeployer: NotebooksDeployer,
        whlDeployer: WhlDeployer,
    ):
        self.__projectBasePath = Path(projectBasePath)
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
