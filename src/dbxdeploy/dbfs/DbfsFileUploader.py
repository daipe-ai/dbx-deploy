from base64 import b64encode
from databricks_api import DatabricksAPI
from dbxdeploy.package.PackageUploaderInterface import PackageUploaderInterface

class DbfsFileUploader(PackageUploaderInterface):

    def __init__(
        self,
        dbxApi: DatabricksAPI
    ):
        self.__dbxApi = dbxApi

    def upload(self, content: bytes, filePath: str, overwrite: bool = False):
        contentToUpload = b64encode(content).decode()

        self.__dbxApi.dbfs.put(
            filePath,
            contents=contentToUpload,
            overwrite=overwrite
        )
