# pylint: disable = too-many-instance-attributes
from logging import Logger
from pathlib import Path
from dbxdeploy.cluster.ClusterRestarter import ClusterRestarter
from dbxdeploy.deploy.CurrentAndReleaseDeployer import CurrentAndReleaseDeployer
from dbxdeploy.job.JobsCreatorAndRunner import JobsCreatorAndRunner
from dbxdeploy.job.JobsDeleter import JobsDeleter
from dbxdeploy.notebook.NotebooksLocator import NotebooksLocator
from dbxdeploy.package.PackageMetadataLoader import PackageMetadataLoader
from dbxdeploy.whl.WhlDeployer import WhlDeployer
import asyncio

class DeployWithCleanup:

    def __init__(
        self,
        projectBasePath: Path,
        logger: Logger,
        packageMetadataLoader: PackageMetadataLoader,
        currentAndReleaseDeployer: CurrentAndReleaseDeployer,
        whlDeployer: WhlDeployer,
        clusterRestarter: ClusterRestarter,
        jobsDeleter: JobsDeleter,
        jobsCreatorAndRunner: JobsCreatorAndRunner,
        notebooksLocator: NotebooksLocator,
    ):
        self.__projectBasePath = projectBasePath
        self.__logger = logger
        self.__packageMetadataLoader = packageMetadataLoader
        self.__currentAndReleaseDeployer = currentAndReleaseDeployer
        self.__whlDeployer = whlDeployer
        self.__clusterRestarter = clusterRestarter
        self.__jobsDeleter = jobsDeleter
        self.__jobsCreatorAndRunner = jobsCreatorAndRunner
        self.__notebooksLocator = notebooksLocator

    async def deploy(self):
        packageMetadata = self.__packageMetadataLoader.load(self.__projectBasePath)

        loop = asyncio.get_event_loop()

        whlDeployFuture = loop.run_in_executor(None, self.__whlDeployer.deploy, packageMetadata)
        dbcDeployFuture = loop.run_in_executor(None, self.__currentAndReleaseDeployer.deploy, packageMetadata)

        await whlDeployFuture
        await dbcDeployFuture

        self.__logger.info('--')

        self.__clusterRestarter.restart()
        self.__jobsDeleter.removeAll()

        self.__logger.info('--')

        notebooks = self.__notebooksLocator.locateConsumers()
        self.__jobsCreatorAndRunner.createAndRun(notebooks, packageMetadata)

        self.__logger.info('Deployment completed')
