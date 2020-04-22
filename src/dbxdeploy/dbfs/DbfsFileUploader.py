from base64 import b64encode
from logging import Logger
from pathlib import PurePosixPath
from databricks_api import DatabricksAPI

class DbfsFileUploader:

    def __init__(
        self,
        logMessageTemplate: str,
        logger: Logger,
        dbxApi: DatabricksAPI
    ):
        self.__logMessageTemplate = logMessageTemplate
        self.__logger = logger
        self.__dbxApi = dbxApi

    def upload(self, content: bytes, filePath: PurePosixPath):
        contentToUpload = b64encode(content).decode()

        self.__logger.info(self.__logMessageTemplate.format(filePath))

        self.__dbxApi.dbfs.put(
            str(filePath),
            contents=contentToUpload,
            overwrite=True
        )
