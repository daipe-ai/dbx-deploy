from base64 import b64encode
from databricks_api import DatabricksAPI

class WhlUploader:

    def __init__(self, dbfsBasePath, dbxApi: DatabricksAPI):
        self.__dbfsBasePath = dbfsBasePath
        self.__dbxApi = dbxApi

    def upload(self, whlContent: bytes, fileName: str):
        contentToUpload = b64encode(whlContent).decode()

        self.__dbxApi.dbfs.put(
            self.__dbfsBasePath + '/' + fileName,
            contents=contentToUpload,
            overwrite=True
        )
