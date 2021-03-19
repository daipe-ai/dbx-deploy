import asyncio
from argparse import Namespace
from logging import Logger
from dbxdeploy.deploy.Deployer import Deployer
from consolebundle.ConsoleCommand import ConsoleCommand


class DeployCommand(ConsoleCommand):
    def __init__(self, dbx_host: str, workspace_base_dir: str, logger: Logger, deployer: Deployer):
        self.__dbx_host = dbx_host
        self.__workspace_base_dir = workspace_base_dir
        self.__logger = logger
        self.__deployer = deployer

    def get_command(self) -> str:
        return "dbx:deploy"

    def get_description(self):
        return "Deploy notebooks and master package to DBX"

    def run(self, input_args: Namespace):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__deployer.deploy())

        self.__logger.info(f"Deployed to {self.__dbx_host} {self.__workspace_base_dir}")
