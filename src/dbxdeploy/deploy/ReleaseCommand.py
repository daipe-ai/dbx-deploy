import asyncio
from argparse import Namespace
from logging import Logger
from dbxdeploy.deploy.Releaser import Releaser
from consolebundle.ConsoleCommand import ConsoleCommand


class ReleaseCommand(ConsoleCommand):
    def __init__(self, dbx_host: str, workspace_base_dir: str, logger: Logger, releaser: Releaser):
        self.__dbx_host = dbx_host
        self.__workspace_base_dir = workspace_base_dir
        self.__logger = logger
        self.__releaser = releaser

    def get_command(self) -> str:
        return "dbx:release"

    def get_description(self):
        return "Release the app to the production environment"

    def run(self, input_args: Namespace):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__releaser.release())

        self.__logger.info(f"Deployed to {self.__dbx_host}, {self.__workspace_base_dir}")
