from databricks_api import DatabricksAPI
from logging import Logger


class JobsDeleter:
    def __init__(self, logger: Logger, dbx_api: DatabricksAPI):
        self.__logger = logger
        self.__dbx_api = dbx_api

    def remove_all(self):
        def callback(job_id, notebook_path):
            self.__logger.info("Deleting job #{}: {}".format(job_id, notebook_path))
            self.__dbx_api.jobs.delete_job(job_id)

        self.__remove(callback)

    def remove(self, notebook_paths: set):
        def callback(job_id, notebook_path):
            if notebook_path in notebook_paths:
                self.__logger.info("Deleting job #{}: {}".format(job_id, notebook_path))
                self.__dbx_api.jobs.delete_job(job_id)

        self.__remove(callback)

    def __remove(self, callback: callable):
        while True:
            jobs_response = self.__dbx_api.jobs.list_jobs()

            if "jobs" not in jobs_response:
                if "jobs" in locals():
                    self.__logger.info("No more jobs exist")
                else:
                    self.__logger.info("No jobs exist")
                break

            jobs = jobs_response["jobs"]

            self.__logger.info("{} active jobs found".format(len(jobs)))

            for job in jobs:
                job_id = job["job_id"]
                notebook_path = job["settings"]["notebook_task"]["notebook_path"]

                callback(job_id, notebook_path)
