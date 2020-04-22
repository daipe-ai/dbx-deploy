from dbxdeploy.job.NotebookKiller import NotebookKiller
from dbxdeploy.notebook.NotebooksLocator import NotebooksLocator
from dbxdeploy.package.PackageMetadata import PackageMetadata
from dbxdeploy.package.PackageMetadataLoader import PackageMetadataLoader
from dbxdeploy.package.PackageDeployer import PackageDeployer
from dbxdeploy.notebook.NotebooksDeployer import NotebooksDeployer
from dbxdeploy.job.JobSubmitter import JobSubmitter
from pathlib import Path, PurePosixPath
import asyncio

class DeployerJobSubmitter:

    def __init__(
        self,
        projectBaseDir: Path,
        packageMetadataLoader: PackageMetadataLoader,
        notebookKiller: NotebookKiller,
        notebooksDeployer: NotebooksDeployer,
        packageDeployer: PackageDeployer,
        jobSubmitter: JobSubmitter,
        notebooksLocator: NotebooksLocator,
    ):
        self.__projectBaseDir = projectBaseDir
        self.__packageMetadataLoader = packageMetadataLoader
        self.__notebookKiller = notebookKiller
        self.__notebooksDeployer = notebooksDeployer
        self.__packageDeployer = packageDeployer
        self.__jobSubmitter = jobSubmitter
        self.__notebooksLocator = notebooksLocator

    async def deployAndSubmitJob(self, notebookPath: PurePosixPath):
        packageMetadata = self.__packageMetadataLoader.load(self.__projectBaseDir)

        def deployRoot(packageMetadata: PackageMetadata):
            notebooks = self.__notebooksLocator.locate()
            self.__notebooksDeployer.deploy(packageMetadata, notebooks)

        loop = asyncio.get_event_loop()

        notebookKillerFuture = loop.run_in_executor(None, self.__notebookKiller.killIfRunning, notebookPath, packageMetadata)
        packageDeployFuture = loop.run_in_executor(None, self.__packageDeployer.deploy, packageMetadata)
        dbcDeployFuture = loop.run_in_executor(None, deployRoot, packageMetadata)

        await notebookKillerFuture
        await packageDeployFuture
        await dbcDeployFuture

        self.__jobSubmitter.submit(notebookPath, packageMetadata)
