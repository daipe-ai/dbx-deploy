from databricks_api import DatabricksAPI
from logging import Logger

class JobsDeleter:

    def __init__(
        self,
        logger: Logger,
        dbxApi: DatabricksAPI
    ):
        self.__logger = logger
        self.__dbxApi = dbxApi

    def removeAll(self):
        def callback(jobId, notebookPath):
            self.__logger.info('Deleting job #{}: {}'.format(jobId, notebookPath))
            self.__dbxApi.jobs.delete_job(jobId)

        self.__remove(callback)

    def remove(self, notebookPaths: set):
        def callback(jobId, notebookPath):
            if notebookPath in notebookPaths:
                self.__logger.info('Deleting job #{}: {}'.format(jobId, notebookPath))
                self.__dbxApi.jobs.delete_job(jobId)

        self.__remove(callback)

    def __remove(self, callback: callable):
        while True:
            jobsResponse = self.__dbxApi.jobs.list_jobs()

            if 'jobs' not in jobsResponse:
                if 'jobs' in locals():
                    self.__logger.info('No more jobs exist')
                else:
                    self.__logger.info('No jobs exist')
                break

            jobs = jobsResponse['jobs']

            self.__logger.info('{} active jobs found'.format(len(jobs)))

            for job in jobs:
                jobId = job['job_id']
                notebookPath = job['settings']['notebook_task']['notebook_path']

                callback(jobId, notebookPath)
