from base64 import b64encode
from pathlib import PurePosixPath
from databricks_api import DatabricksAPI

class DbfsFileUploader:

    def __init__(
        self,
        dbxApi: DatabricksAPI
    ):
        self.__dbxApi = dbxApi

    def upload(self, content: bytes, filePath: PurePosixPath):
        contentToUpload = b64encode(content).decode()

        self.__dbxApi.dbfs.put(
            str(filePath),
            contents=contentToUpload,
            overwrite=True
        )
