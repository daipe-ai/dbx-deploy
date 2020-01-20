from dbxdeploy.job.NotebookKiller import NotebookKiller
from dbxdeploy.package.PackageMetadataLoader import PackageMetadataLoader
from dbxdeploy.whl.WhlDeployer import WhlDeployer
from dbxdeploy.notebook.NotebooksDeployer import NotebooksDeployer
from dbxdeploy.job.JobSubmitter import JobSubmitter
from pathlib import Path, PurePosixPath
import asyncio

class DeployerJobSubmitter:

    def __init__(
        self,
        projectBasePath: Path,
        packageMetadataLoader: PackageMetadataLoader,
        notebookKiller: NotebookKiller,
        notebooksDeployer: NotebooksDeployer,
        whlDeployer: WhlDeployer,
        jobSubmitter: JobSubmitter,
    ):
        self.__projectBasePath = projectBasePath
        self.__packageMetadataLoader = packageMetadataLoader
        self.__notebookKiller = notebookKiller
        self.__notebooksDeployer = notebooksDeployer
        self.__whlDeployer = whlDeployer
        self.__jobSubmitter = jobSubmitter

    async def deployAndSubmitJob(self, notebookPath: PurePosixPath):
        packageMetadata = self.__packageMetadataLoader.load(self.__projectBasePath)

        loop = asyncio.get_event_loop()

        notebookKillerFuture = loop.run_in_executor(None, self.__notebookKiller.killIfRunning, notebookPath, packageMetadata)
        whlDeployFuture = loop.run_in_executor(None, self.__whlDeployer.deploy, packageMetadata)
        dbcDeployFuture = loop.run_in_executor(None, self.__notebooksDeployer.deploy, packageMetadata)

        await notebookKillerFuture
        await whlDeployFuture
        await dbcDeployFuture

        self.__jobSubmitter.submit(notebookPath, packageMetadata)
