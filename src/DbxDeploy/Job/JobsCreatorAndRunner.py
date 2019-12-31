from typing import List
from databricks_api.databricks import DatabricksAPI
from DbxDeploy.Job.JobCreator import JobCreator
from DbxDeploy.Notebook.Notebook import Notebook
from DbxDeploy.Package.PackageMetadata import PackageMetadata
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

    def createAndRun(self, notebooks: List[Notebook], packageMetadata: PackageMetadata):
        createdJobs = list(map(lambda notebook: self.__jobCreator.create(notebook.databricksRelativePath, packageMetadata), notebooks))

        self.__logger.info('--')

        for createdJob in createdJobs:
            jobId = createdJob['job_id']
            notebookReleasePath = createdJob['notebook_release_path']

            self.__logger.info('Running job #{}: {}'.format(jobId, notebookReleasePath))
            self.__dbxApi.jobs.run_now(jobId)

        self.__logger.info('--')
