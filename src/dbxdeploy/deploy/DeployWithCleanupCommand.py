import asyncio
from argparse import Namespace
from dbxdeploy.deploy.DeployWithCleanup import DeployWithCleanup
from consolebundle.ConsoleCommand import ConsoleCommand

class DeployWithCleanupCommand(ConsoleCommand):

    def __init__(
        self,
        deployWithCleanup: DeployWithCleanup
    ):
        self.__deployWithCleanup = deployWithCleanup

    def getCommand(self) -> str:
        return 'dbx:deploy:with-cleanup'

    def getDescription(self):
        return 'Deploy with cleanup'

    def run(self, inputArgs: Namespace):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__deployWithCleanup.deploy())
