from logging import Logger
from typing import Optional, Dict

from dbxdeploy.utils.DatabricksClient import DatabricksClient


class JobGetter:
    def __init__(
        self,
        logger: Logger,
        dbx_api: DatabricksClient,
    ):
        self.__logger = logger
        self.__dbx_api = dbx_api

    def get_job_id_by_name(self, job_name: str) -> Optional[int]:
        job_id = None
        jobs_response = self.__dbx_api.jobs.list_jobs()

        if "jobs" not in jobs_response:
            self.__logger.error("No jobs exist")
            return job_id

        jobs = jobs_response["jobs"]

        for job in jobs:
            if job["settings"]["name"] == job_name:
                job_id = job["job_id"]
        return job_id

    def get_run_state(self, run_id: int) -> Dict:
        return self.__dbx_api.jobs.get_run(run_id=run_id)["state"]
