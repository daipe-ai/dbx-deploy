from logging import Logger
from pathlib import PurePosixPath, Path
from DbxDeploy.Cluster.ClusterRestarter import ClusterRestarter
from DbxDeploy.Job.JobsCreatorAndRunner import JobsCreatorAndRunner
from DbxDeploy.Job.JobsDeleter import JobsDeleter
from DbxDeploy.Setup.SetupLoader import SetupLoader
from DbxDeploy.Whl.WhlDeployer import WhlDeployer
from DbxDeploy.Dbc.DbcDeployer import DbcDeployer
import asyncio

class DeployWithCleanup:

    def __init__(
        self,
        projectBasePath: str,
        setupLoader: SetupLoader,
        dbcDeployer: DbcDeployer,
        whlDeployer: WhlDeployer,
        clusterRestarter: ClusterRestarter,
        jobsDeleter: JobsDeleter,
        jobsCreatorAndRunner: JobsCreatorAndRunner,
        logger: Logger,
    ):
        self.__projectBasePath = Path(projectBasePath)
        self.__setupLoader = setupLoader
        self.__dbcDeployer = dbcDeployer
        self.__whlDeployer = whlDeployer
        self.__clusterRestarter = clusterRestarter
        self.__jobsDeleter = jobsDeleter
        self.__jobsCreatorAndRunner = jobsCreatorAndRunner
        self.__logger = logger

    async def deploy(self):
        setup = self.__setupLoader.load(self.__projectBasePath)
        packageMetadata = setup.getPackageMetadata()

        loop = asyncio.get_event_loop()

        whlDeployFuture = loop.run_in_executor(None, self.__whlDeployer.deploy, setup, packageMetadata)
        dbcDeployFuture = loop.run_in_executor(None, self.__dbcDeployer.deploy, packageMetadata)

        await whlDeployFuture
        await dbcDeployFuture

        self.__logger.info('--')

        self.__clusterRestarter.restart()
        self.__jobsDeleter.removeAll()

        self.__logger.info('--')

        notebookPaths = []

        for path in self.__projectBasePath.joinpath('src').glob('**/*.ipynb'):
            notebookPath = path.relative_to(self.__projectBasePath.joinpath('src')).with_suffix('')
            notebookPaths.append(PurePosixPath(notebookPath))

        self.__jobsCreatorAndRunner.createAndRun(notebookPaths, packageMetadata.getVersion())

        self.__logger.info('Deployment completed')
