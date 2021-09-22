import asyncio
from argparse import Namespace, ArgumentParser
from logging import Logger
from pathlib import PurePosixPath
from typing import Optional
from dbxdeploy.deploy.Releaser import Releaser
from consolebundle.ConsoleCommand import ConsoleCommand


class ReleaseCommand(ConsoleCommand):
    def __init__(self, cluster_id: Optional[str], dbx_host: str, workspace_base_dir: PurePosixPath, logger: Logger, releaser: Releaser):
        self.__cluster_id = cluster_id
        self.__dbx_host = dbx_host
        self.__workspace_base_dir = workspace_base_dir
        self.__logger = logger
        self.__releaser = releaser

    def get_command(self) -> str:
        return "dbx:release"

    def get_description(self):
        return "Release the app to the production environment"

    def configure(self, argument_parser: ArgumentParser):
        # deprecated, will be removed in 2.0; use CLI argument to defined cluster_id instead
        if self.__cluster_id is None:
            argument_parser.add_argument(dest="cluster_id", help="Cluster to be restarted before release finishes")

    def run(self, input_args: Namespace):
        cluster_id = self.__cluster_id if self.__cluster_id is not None else input_args.cluster_id

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__releaser.release(cluster_id))

        self.__logger.info(f"Released to {self.__dbx_host}/#workspace{self.__workspace_base_dir}")
