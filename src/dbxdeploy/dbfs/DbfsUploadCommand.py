import os
from argparse import Namespace, ArgumentParser
from logging import Logger
from consolebundle.ConsoleCommand import ConsoleCommand
from consolebundle.StrToBool import str2Bool
from databricks_cli.dbfs.api import DbfsApi
from databricks_cli.dbfs.dbfs_path import DbfsPath

class DbfsUploadCommand(ConsoleCommand):

    def __init__(
        self,
        logger: Logger,
        dbfsApi: DbfsApi,
    ):
        self.__logger = logger
        self.__dbfsApi = dbfsApi

    def getCommand(self) -> str:
        return 'dbx:dbfs:upload'

    def getDescription(self):
        return 'Uploads file to DBFS'

    def configure(self, argumentParser: ArgumentParser):
        argumentParser.add_argument(dest='sourceFilePath', help='Source file path')
        argumentParser.add_argument(dest='targetFilePath', help='Target file path')
        argumentParser.add_argument('--overwrite', dest='overwrite', type=str2Bool, nargs='?', const=True, default=False, help='Overwrite target file')

    def run(self, inputArgs: Namespace):
        if os.path.isabs(inputArgs.sourceFilePath):
            sourceFilePath = inputArgs.sourceFilePath
        else:
            sourceFilePath = os.getcwd() + os.sep + inputArgs.sourceFilePath

        self.__logger.info(f'Uploading {sourceFilePath} to {inputArgs.targetFilePath}')

        self.__dbfsApi.put_file(
            sourceFilePath,
            DbfsPath(inputArgs.targetFilePath),
            inputArgs.overwrite,
        )

        self.__logger.info(f'File successfully uploaded')
