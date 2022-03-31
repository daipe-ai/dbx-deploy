import sys
import time
from logging import Logger
from argparse import Namespace, ArgumentParser
from consolebundle.ConsoleCommand import ConsoleCommand

from dbxdeploy.job.JobGetter import JobGetter
from dbxdeploy.utils.DatabricksClient import DatabricksClient


class FollowRunCommand(ConsoleCommand):
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

    def get_command(self) -> str:
        return "dbx:job:follow-run"

    def get_description(self):
        return "Follow an active job run by job_name"

    def run(self, input_args: Namespace):
        job_name = input_args.job_name
        run_id = self.__job_getter.get_active_run_id_by_job_name(job_name)

        if not run_id:
            self.__logger.error(f"Active run of the job `{job_name}` doesn't exist")
            return

        state = self.__job_getter.get_run_state(run_id)

        timer = 0
        while "result_state" not in state and timer < self.__time_limit:
            self.__logger.info(state["life_cycle_state"])
            time.sleep(self.__refresh_period)
            timer += self.__refresh_period
            state = self.__job_getter.get_run_state(run_id)

        if not state["result_state"] == "SUCCESS":
            run = self.__dbx_api.jobs.get_run(run_id=run_id)
            self.__logger.error(f"Job run {run_id}: {run['run_page_url']} was not successful.")
            sys.exit(1)
