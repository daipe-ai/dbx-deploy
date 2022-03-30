import sys
import time
from logging import Logger
from argparse import Namespace, ArgumentParser
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.utils.DatabricksClient import DatabricksClient


class FollowRunCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        dbx_api: DatabricksClient,
        period: int,
        limit: int,
    ):
        self.__logger = logger
        self.__dbx_api = dbx_api
        self.__period = period
        self.__limit = limit

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument(dest="run_id", help="Databricks job run_id")

    def get_command(self) -> str:
        return "dbx:follow-run"

    def get_description(self):
        return "Follow a job run by job_id"

    def run(self, input_args: Namespace):
        def get_run_state(run_id: str):
            return self.__dbx_api.jobs.get_run(run_id=run_id)["state"]

        run_id = input_args.run_id
        state = get_run_state(run_id)

        timer = 0
        while "result_state" not in state and timer < self.__limit:
            self.__logger.info(state["life_cycle_state"])
            time.sleep(self.__period)
            timer += self.__period
            state = get_run_state(run_id)

        if not state["result_state"] == "SUCCESS":
            run = self.__dbx_api.jobs.get_run(run_id=run_id)
            self.__logger.error(f"Job run {run_id}: {run['run_page_url']} was not successful.")
            sys.exit(1)
