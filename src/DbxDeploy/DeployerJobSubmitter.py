from DbxDeploy.Job.NotebookKiller import NotebookKiller
from DbxDeploy.Setup.SetupLoader import SetupLoader
from DbxDeploy.Whl.WhlDeployer import WhlDeployer
from DbxDeploy.Dbc.DbcDeployer import DbcDeployer
from DbxDeploy.Job.JobSubmitter import JobSubmitter
from pathlib import Path, PurePosixPath

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

    def deployAndSubmitJob(self, notebookPath: PurePosixPath):
        setup = self.__setupLoader.load(self.__projectBasePath)
        packageMetadata = setup.getPackageMetadata()

        self.__notebookKiller.killIfRunning(notebookPath, packageMetadata.getVersion())
        self.__whlDeployer.deploy(setup, packageMetadata)
        self.__dbcDeployer.deploy(packageMetadata)
        self.__jobSubmitter.submit(notebookPath, packageMetadata.getVersion())
