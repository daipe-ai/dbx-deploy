import asyncio
from argparse import Namespace
from logging import Logger
from dbxdeploy.deploy.Deployer import Deployer
from consolebundle.ConsoleCommand import ConsoleCommand

class DeployCommand(ConsoleCommand):

    def __init__(
        self,
        dbxHost: str,
        workspaceBaseDir: str,
        logger: Logger,
        deployer: Deployer
    ):
        self.__dbxHost = dbxHost
        self.__workspaceBaseDir = workspaceBaseDir
        self.__logger = logger
        self.__deployer = deployer

    def getCommand(self) -> str:
        return 'dbx:deploy'

    def getDescription(self):
        return 'Deploy notebooks and master package to DBX'

    def run(self, inputArgs: Namespace):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__deployer.deploy())

        self.__logger.info(f'Deployed to {self.__dbxHost}, {self.__workspaceBaseDir}')
