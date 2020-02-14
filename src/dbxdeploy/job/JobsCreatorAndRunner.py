from typing import List
from databricks_api.databricks import DatabricksAPI
from dbxdeploy.job.JobCreator import JobCreator
from dbxdeploy.notebook.Notebook import Notebook
from dbxdeploy.package.PackageMetadata import PackageMetadata
from logging import Logger

class JobsCreatorAndRunner:

    def __init__(
        self,
        logger: Logger,
        dbxApi: DatabricksAPI,
        jobCreator: JobCreator,
    ):
        self.__logger = logger
        self.__dbxApi = dbxApi
        self.__jobCreator = jobCreator

    def createAndRun(self, notebooks: List[Notebook], packageMetadata: PackageMetadata):
        createdJobs = list(map(lambda notebook: self.__jobCreator.create(notebook.databricksRelativePath, packageMetadata), notebooks))

        self.__logger.info('--')

        for createdJob in createdJobs:
            jobId = createdJob['job_id']
            notebookReleasePath = createdJob['notebook_release_path']

            self.__logger.info('Running job #{}: {}'.format(jobId, notebookReleasePath))
            self.__dbxApi.jobs.run_now(jobId)

        self.__logger.info('--')
