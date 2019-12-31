from base64 import b64encode
from logging import Logger
from pathlib import PurePosixPath
from databricks_api import DatabricksAPI

class WhlUploader:

    def __init__(
        self,
        logger: Logger,
        dbxApi: DatabricksAPI
    ):
        self.__logger = logger
        self.__dbxApi = dbxApi

    def upload(self, whlContent: bytes, filePath: PurePosixPath):
        contentToUpload = b64encode(whlContent).decode()

        self.__logger.info('Uploading app package to {}'.format(filePath))

        self.__dbxApi.dbfs.put(
            str(filePath),
            contents=contentToUpload,
            overwrite=True
        )
