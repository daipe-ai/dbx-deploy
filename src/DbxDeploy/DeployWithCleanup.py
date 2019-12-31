# pylint: disable = too-many-instance-attributes
from logging import Logger
from pathlib import Path
from DbxDeploy.Cluster.ClusterRestarter import ClusterRestarter
from DbxDeploy.Job.JobsCreatorAndRunner import JobsCreatorAndRunner
from DbxDeploy.Job.JobsDeleter import JobsDeleter
from DbxDeploy.Notebook.NotebooksLocator import NotebooksLocator
from DbxDeploy.Package.PackageMetadataLoader import PackageMetadataLoader
from DbxDeploy.Whl.WhlDeployer import WhlDeployer
from DbxDeploy.Notebook.NotebooksDeployer import NotebooksDeployer
import asyncio

class DeployWithCleanup:

    def __init__(
        self,
        projectBasePath: str,
        packageMetadataLoader: PackageMetadataLoader,
        notebooksDeployer: NotebooksDeployer,
        whlDeployer: WhlDeployer,
        clusterRestarter: ClusterRestarter,
        jobsDeleter: JobsDeleter,
        jobsCreatorAndRunner: JobsCreatorAndRunner,
        logger: Logger,
        notebooksLocator: NotebooksLocator,
    ):
        self.__projectBasePath = Path(projectBasePath)
        self.__packageMetadataLoader = packageMetadataLoader
        self.__notebooksDeployer = notebooksDeployer
        self.__whlDeployer = whlDeployer
        self.__clusterRestarter = clusterRestarter
        self.__jobsDeleter = jobsDeleter
        self.__jobsCreatorAndRunner = jobsCreatorAndRunner
        self.__logger = logger
        self.__notebooksLocator = notebooksLocator

    async def deploy(self):
        packageMetadata = self.__packageMetadataLoader.load(self.__projectBasePath)

        loop = asyncio.get_event_loop()

        whlDeployFuture = loop.run_in_executor(None, self.__whlDeployer.deploy, packageMetadata)
        dbcDeployFuture = loop.run_in_executor(None, self.__notebooksDeployer.deployWithCurrent, packageMetadata)

        await whlDeployFuture
        await dbcDeployFuture

        self.__logger.info('--')

        self.__clusterRestarter.restart()
        self.__jobsDeleter.removeAll()

        self.__logger.info('--')

        notebooks = self.__notebooksLocator.locateConsumers()
        self.__jobsCreatorAndRunner.createAndRun(notebooks, packageMetadata)

        self.__logger.info('Deployment completed')
