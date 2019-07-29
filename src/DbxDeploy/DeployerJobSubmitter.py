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
        dbcDeployer: DbcDeployer,
        whlDeployer: WhlDeployer,
        jobSubmitter: JobSubmitter,
    ):
        self.__projectBasePath = Path(projectBasePath)
        self.__setupLoader = setupLoader
        self.__dbcDeployer = dbcDeployer
        self.__whlDeployer = whlDeployer
        self.__jobSubmitter = jobSubmitter

    def deployAndSubmitJob(self, notebookPath: PurePosixPath):
        setup = self.__setupLoader.load(self.__projectBasePath)
        packageMetadata = setup.getPackageMetadata()

        self.__whlDeployer.deploy(setup, packageMetadata)
        self.__dbcDeployer.deploy(packageMetadata)
        self.__jobSubmitter.submit(notebookPath, packageMetadata.getVersion())
