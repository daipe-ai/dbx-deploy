from DbxDeploy.Setup.SetupLoader import SetupLoader
from DbxDeploy.Whl.WhlDeployer import WhlDeployer
from DbxDeploy.Notebook.NotebooksDeployer import NotebooksDeployer
from pathlib import Path
import asyncio

class Deployer:

    def __init__(
        self,
        projectBasePath: str,
        setupLoader: SetupLoader,
        notebooksDeployer: NotebooksDeployer,
        whlDeployer: WhlDeployer,
    ):
        self.__projectBasePath = Path(projectBasePath)
        self.__setupLoader = setupLoader
        self.__notebooksDeployer = notebooksDeployer
        self.__whlDeployer = whlDeployer

    async def deploy(self):
        setup = self.__setupLoader.load(self.__projectBasePath)
        packageMetadata = setup.getPackageMetadata()

        loop = asyncio.get_event_loop()

        whlDeployFuture = loop.run_in_executor(None, self.__whlDeployer.deploy, setup, packageMetadata)
        dbcDeployFuture = loop.run_in_executor(None, self.__notebooksDeployer.deployWithCurrent, packageMetadata)

        await whlDeployFuture
        await dbcDeployFuture
