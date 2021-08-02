from logging import Logger
from argparse import Namespace, ArgumentParser
from typing import Optional
from dbxdeploy.job.JobsDeleter import JobsDeleter
from dbxdeploy.cluster.ClusterRestarter import ClusterRestarter
from consolebundle.ConsoleCommand import ConsoleCommand


class JobsDeleterCommand(ConsoleCommand):
    def __init__(
        self,
        cluster_id: Optional[str],
        logger: Logger,
        cluster_restarter: ClusterRestarter,
        jobs_deleter: JobsDeleter,
    ):
        self.__cluster_id = cluster_id
        self.__logger = logger
        self.__cluster_restarter = cluster_restarter
        self.__jobs_deleter = jobs_deleter

    def get_command(self) -> str:
        return "dbx:jobs:delete-all"

    def get_description(self):
        return "Deletes all DBX jobs"

    def configure(self, argument_parser: ArgumentParser):
        # deprecated, will be removed in 2.0; use CLI argument to defined cluster_id instead
        if self.__cluster_id is None:
            argument_parser.add_argument(dest="cluster_id", help="Cluster to be restarted before job deletion starts")

    def run(self, input_args: Namespace):
        self.__logger.info("Jobs deletion started")

        cluster_id = self.__cluster_id if self.__cluster_id is not None else input_args.cluster_id

        self.__cluster_restarter.restart(cluster_id)
        self.__jobs_deleter.remove_all()
