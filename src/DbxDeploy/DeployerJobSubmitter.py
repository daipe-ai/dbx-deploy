from DbxDeploy.Deployer import Deployer
from DbxDeploy.Job.JobSubmitter import JobSubmitter
from pathlib import PurePosixPath

class DeployerJobSubmitter:

    def __init__(self,
        deployer: Deployer,
        jobSubmitter: JobSubmitter,
    ):
        self.__deployer = deployer
        self.__jobSubmitter = jobSubmitter

    def deployAndSubmitJob(self, notebookPath: PurePosixPath):
        packageMetadata = self.__deployer.deploy()
        self.__jobSubmitter.submit(notebookPath, packageMetadata.version)
