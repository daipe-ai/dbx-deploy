import asyncio
from argparse import Namespace
from logging import Logger
from dbxdeploy.deploy.Releaser import Releaser
from consolebundle.ConsoleCommand import ConsoleCommand

class ReleaseCommand(ConsoleCommand):

    def __init__(
        self,
        dbxHost: str,
        workspaceBaseDir: str,
        logger: Logger,
        releaser: Releaser
    ):
        self.__dbxHost = dbxHost
        self.__workspaceBaseDir = workspaceBaseDir
        self.__logger = logger
        self.__releaser = releaser

    def getCommand(self) -> str:
        return 'dbx:release'

    def getDescription(self):
        return 'Release the app to the production environment'

    def run(self, inputArgs: Namespace):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__releaser.release())

        self.__logger.info(f'Deployed to {self.__dbxHost}, {self.__workspaceBaseDir}')
