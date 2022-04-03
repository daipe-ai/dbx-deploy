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
        argument_parser.add_argument("--wait", action="store_true", dest="wait", help="Whether to wait for the run to finish or not")
        argument_parser.add_argument(
            "--time-limit",
            dest="time_limit",
            default=self.__time_limit,
            type=int,
            help="How long to wait for the run to finish, default from config",
        )

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

        if input_args.wait:
            self.__wait_for_run_to_finish(run, input_args.time_limit)

    def __wait_for_run_to_finish(self, run: Dict, time_limit: int):
        run_id = run["run_id"]
        state = self.__job_getter.get_run_state(run_id)

        def is_finished(state: Dict) -> bool:
            return "result_state" in state or state["life_cycle_state"] == "SKIPPED"

        timer = 0
        while not is_finished(state) and timer < time_limit:
            self.__logger.info(f"{state['life_cycle_state']} - {run['run_page_url']}")
            time.sleep(self.__refresh_period)
            timer += self.__refresh_period
            state = self.__job_getter.get_run_state(run_id)

        def is_success(state: Dict) -> bool:
            return "result_state" in state and state["result_state"] == "SUCCESS"

        if not is_success(state):
            self.__handle_fail(run, state)

    def __handle_fail(self, run: Dict, state: Dict):
        def log(run: Dict):
            return f"Job run {run['run_id']}: {run['run_page_url']}"

        if state["life_cycle_state"] == "SKIPPED":
            self.__logger.error(f"{log(run)} was skipped")
        elif "result_state" not in state:
            self.__logger.error(f"{log(run)} did not finish in time limit")
        elif not state["result_state"] == "SUCCESS":
            self.__logger.error(f"{log(run)} was not successful")
        else:
            self.__logger.error(f"{log(run)} failed due to unknown error:\n{state}")

        sys.exit(1)
