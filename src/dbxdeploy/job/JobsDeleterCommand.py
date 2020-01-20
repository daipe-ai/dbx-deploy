from logging import Logger
from argparse import Namespace
from dbxdeploy.job.JobsDeleter import JobsDeleter
from dbxdeploy.cluster.ClusterRestarter import ClusterRestarter
from consolebundle.ConsoleCommand import ConsoleCommand

class JobsDeleterCommand(ConsoleCommand):

    def __init__(
        self,
        logger: Logger,
        clusterRestarter: ClusterRestarter,
        jobsDeleter: JobsDeleter,
    ):
        self.__logger = logger
        self.__clusterRestarter = clusterRestarter
        self.__jobsDeleter = jobsDeleter

    def getCommand(self) -> str:
        return 'dbx:jobs:delete-all'

    def getDescription(self):
        return 'Deletes all DBX jobs'

    def run(self, inputArgs: Namespace):
        self.__logger.info('Jobs deletion started')

        self.__clusterRestarter.restart()
        self.__jobsDeleter.removeAll()
