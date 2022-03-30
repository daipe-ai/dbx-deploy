from logging import Logger
from argparse import Namespace, ArgumentParser
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.utils.DatabricksClient import DatabricksClient


class RunJobCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        dbx_api: DatabricksClient,
    ):
        self.__logger = logger
        self.__dbx_api = dbx_api

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument(dest="job_name", help="Databricks job name")

    def get_command(self) -> str:
        return "dbx:run-job"

    def get_description(self):
        return "Run a job by a name"

    def run(self, input_args: Namespace):
        job_name = input_args.job_name
        self.__logger.info(f"Job name `{job_name}`")

        jobs_response = self.__dbx_api.jobs.list_jobs()["jobs"]

        if "jobs" not in jobs_response:
            self.__logger.error("No jobs exist")
            return

        jobs = jobs_response["jobs"]

        job_id = None
        for job in jobs:
            if job["settings"]["name"] == job_name:
                job_id = job["job_id"]

        if not job_id:
            self.__logger.error(f"Job with the name `{job_name}` doesn't exist")
            return

        self.__logger.info("Initiating run...")

        run = self.__dbx_api.jobs.run_now(job_id=job_id)

        run = self.__dbx_api.jobs.get_run(run_id=run["run_id"])
        self.__logger.info(f"Run of `{job_name}` running at {run['run_page_url']}")
