from logging import Logger
from argparse import Namespace
from dbxdeploy.job.JobsDeleter import JobsDeleter
from dbxdeploy.cluster.ClusterRestarter import ClusterRestarter
from consolebundle.ConsoleCommand import ConsoleCommand


class JobsDeleterCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        cluster_restarter: ClusterRestarter,
        jobs_deleter: JobsDeleter,
    ):
        self.__logger = logger
        self.__cluster_restarter = cluster_restarter
        self.__jobs_deleter = jobs_deleter

    def get_command(self) -> str:
        return "dbx:jobs:delete-all"

    def get_description(self):
        return "Deletes all DBX jobs"

    def run(self, input_args: Namespace):
        self.__logger.info("Jobs deletion started")

        self.__cluster_restarter.restart()
        self.__jobs_deleter.remove_all()
