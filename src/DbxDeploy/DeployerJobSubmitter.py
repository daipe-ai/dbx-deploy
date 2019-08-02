from DbxDeploy.Job.NotebookKiller import NotebookKiller
from DbxDeploy.Setup.SetupLoader import SetupLoader
from DbxDeploy.Whl.WhlDeployer import WhlDeployer
from DbxDeploy.Dbc.DbcDeployer import DbcDeployer
from DbxDeploy.Job.JobSubmitter import JobSubmitter
from pathlib import Path, PurePosixPath
import asyncio

class DeployerJobSubmitter:

    def __init__(
        self,
        projectBasePath: str,
        setupLoader: SetupLoader,
        notebookKiller: NotebookKiller,
        dbcDeployer: DbcDeployer,
        whlDeployer: WhlDeployer,
        jobSubmitter: JobSubmitter,
    ):
        self.__projectBasePath = Path(projectBasePath)
        self.__setupLoader = setupLoader
        self.__notebookKiller = notebookKiller
        self.__dbcDeployer = dbcDeployer
        self.__whlDeployer = whlDeployer
        self.__jobSubmitter = jobSubmitter

    async def deployAndSubmitJob(self, notebookPath: PurePosixPath):
        setup = self.__setupLoader.load(self.__projectBasePath)
        packageMetadata = setup.getPackageMetadata()

        loop = asyncio.get_event_loop()

        notebookKillerFuture = loop.run_in_executor(None, self.__notebookKiller.killIfRunning, notebookPath, packageMetadata.getVersion())
        whlDeployFuture = loop.run_in_executor(None, self.__whlDeployer.deploy, setup, packageMetadata)
        dbcDeployFuture = loop.run_in_executor(None, self.__dbcDeployer.deploy, packageMetadata)

        await notebookKillerFuture
        await whlDeployFuture
        await dbcDeployFuture

        self.__jobSubmitter.submit(notebookPath, packageMetadata.getVersion())
