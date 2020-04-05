import asyncio
from argparse import Namespace
from dbxdeploy.deploy.Releaser import Releaser
from consolebundle.ConsoleCommand import ConsoleCommand

class ReleaseCommand(ConsoleCommand):

    def __init__(
        self,
        releaser: Releaser
    ):
        self.__releaser = releaser

    def getCommand(self) -> str:
        return 'dbx:release'

    def getDescription(self):
        return 'Release the app to the production environment'

    def run(self, inputArgs: Namespace):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__releaser.release())
