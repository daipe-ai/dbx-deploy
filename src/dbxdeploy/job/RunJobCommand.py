import sys
import time

from logging import Logger
from argparse import Namespace, ArgumentParser
from typing import Dict

from consolebundle.ConsoleCommand import ConsoleCommand

from dbxdeploy.job.JobGetter import JobGetter
from dbxdeploy.utils.DatabricksClient import DatabricksClient


class RunJobCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        dbx_api: DatabricksClient,
        refresh_period: int,
        time_limit: int,
        job_getter: JobGetter,
    ):
        self.__logger = logger
        self.__dbx_api = dbx_api
        self.__refresh_period = refresh_period
        self.__time_limit = time_limit
        self.__job_getter = job_getter

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument("--job-name", dest="job_name", help="Databricks job name")
        argument_parser.add_argument("--follow", action="store_true", dest="follow", help="Whether to wait for the run to finish or not")

    def get_command(self) -> str:
        return "dbx:job:run"

    def get_description(self):
        return "Run a job by a name"

    def run(self, input_args: Namespace):
        job_name = input_args.job_name
        self.__logger.info(f"Job name `{job_name}`")
        job_id = self.__job_getter.get_job_id_by_name(job_name)

        if not job_id:
            self.__logger.error(f"Job with the name `{job_name}` doesn't exist")
            return

        self.__logger.info("Initiating run...")

        run_init = self.__dbx_api.jobs.run_now(job_id=job_id)
        run = self.__dbx_api.jobs.get_run(run_id=run_init["run_id"])

        self.__logger.info(f"Run of `{job_name}` running at {run['run_page_url']}")

        if input_args.follow:
            self.__follow_run(run)

    def __follow_run(self, run: Dict):
        run_id = run["run_id"]
        state = self.__job_getter.get_run_state(run_id)

        timer = 0
        while "result_state" not in state and timer < self.__time_limit:
            self.__logger.info(f"{state['life_cycle_state']} - {run['run_page_url']}")
            time.sleep(self.__refresh_period)
            timer += self.__refresh_period
            state = self.__job_getter.get_run_state(run_id)

        if "result_state" not in state:
            self.__logger.error(f"Job run {run_id}: {run['run_page_url']} did not finish in time limit.")
            sys.exit(1)

        if not state["result_state"] == "SUCCESS":
            self.__logger.error(f"Job run {run_id}: {run['run_page_url']} was not successful.")
            sys.exit(1)
