import asyncio
from argparse import Namespace
from dbxdeploy.deploy.Deployer import Deployer
from consolebundle.ConsoleCommand import ConsoleCommand

class DeployCommand(ConsoleCommand):

    def __init__(
        self,
        deployer: Deployer
    ):
        self.__deployer = deployer

    def getCommand(self) -> str:
        return 'dbx:deploy'

    def getDescription(self):
        return 'Deploy to DBX'

    def run(self, inputArgs: Namespace):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__deployer.deploy())
