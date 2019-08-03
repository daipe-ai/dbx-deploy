from databricks_api.databricks import DatabricksAPI
from DbxDeploy.Job.JobCreator import JobCreator
from DbxDeploy.Setup.Version.VersionInterface import VersionInterface
from logging import Logger

class JobsCreatorAndRunner:

    def __init__(
        self,
        logger: Logger,
        jobCreator: JobCreator,
        dbxApi: DatabricksAPI
    ):
        self.__logger = logger
        self.__jobCreator = jobCreator
        self.__dbxApi = dbxApi

    def createAndRun(self, notebookPaths: list, version: VersionInterface):
        createdJobs = []

        for notebookPath in notebookPaths:
            job = self.__jobCreator.create(notebookPath, version)
            createdJobs.append(job)

        self.__logger.info('--')

        for createdJob in createdJobs:
            jobId = createdJob['job_id']
            notebookReleasePath = createdJob['notebook_release_path']

            self.__logger.info('Running job #{}: {}'.format(jobId, notebookReleasePath))
            self.__dbxApi.jobs.run_now(jobId)

        self.__logger.info('--')
