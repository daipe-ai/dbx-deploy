from base64 import b64encode
from logging import Logger
from databricks_api import DatabricksAPI

class WhlUploader:

    def __init__(
        self,
        dbfsBasePath: str,
        logger: Logger,
        dbxApi: DatabricksAPI
    ):
        self.__dbfsBasePath = dbfsBasePath
        self.__logger = logger
        self.__dbxApi = dbxApi

    def upload(self, whlContent: bytes, fileName: str):
        contentToUpload = b64encode(whlContent).decode()
        filePath = self.__dbfsBasePath + '/' + fileName

        self.__logger.info('Uploading app package to {}'.format(filePath))

        self.__dbxApi.dbfs.put(
            filePath,
            contents=contentToUpload,
            overwrite=True
        )
