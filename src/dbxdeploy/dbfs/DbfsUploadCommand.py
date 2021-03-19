import os
from argparse import Namespace, ArgumentParser
from logging import Logger
from consolebundle.ConsoleCommand import ConsoleCommand
from consolebundle.StrToBool import str2_bool
from databricks_cli.dbfs.api import DbfsApi
from databricks_cli.dbfs.dbfs_path import DbfsPath


class DbfsUploadCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        dbfs_api: DbfsApi,
    ):
        self.__logger = logger
        self.__dbfs_api = dbfs_api

    def get_command(self) -> str:
        return "dbx:dbfs:upload"

    def get_description(self):
        return "Uploads file to DBFS"

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument(dest="source_file_path", help="Source file path")
        argument_parser.add_argument(dest="target_file_path", help="Target file path")
        argument_parser.add_argument(
            "--overwrite", dest="overwrite", type=str2_bool, nargs="?", const=True, default=False, help="Overwrite target file"
        )

    def run(self, input_args: Namespace):
        if os.path.isabs(input_args.source_file_path):
            source_file_path = input_args.source_file_path
        else:
            source_file_path = os.getcwd() + os.sep + input_args.source_file_path

        self.__logger.info(f"Uploading {source_file_path} to {input_args.target_file_path}")

        self.__dbfs_api.put_file(
            source_file_path,
            DbfsPath(input_args.target_file_path),
            input_args.overwrite,
        )

        self.__logger.info("File successfully uploaded")
