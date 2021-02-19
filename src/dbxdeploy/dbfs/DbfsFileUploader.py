from base64 import b64encode
from databricks_api import DatabricksAPI
from dbxdeploy.package.PackageUploaderInterface import PackageUploaderInterface
from requests.exceptions import HTTPError

class DbfsFileUploader(PackageUploaderInterface):

    def __init__(
        self,
        dbxApi: DatabricksAPI
    ):
        self.__dbxApi = dbxApi

    def upload(self, content: bytes, filePath: str, overwrite: bool = False):
        self.__streamingUpload(content, filePath, overwrite)

    def exists(self, filePath: str):
        try:
            self.__dbxApi.dbfs.get_status(filePath)

        except HTTPError as ex:
            if ex.response.status_code != 404:
                raise

            return False

        return True

    def __streamingUpload(self, content: bytes, filePath: str, overwrite: bool = False):
        response = self.__dbxApi.dbfs.create(filePath, overwrite=overwrite)
        handle = response['handle']

        chunkSize = int(0.5 * 1024 * 1024) # 0.5MiB

        for chunk in self.__chunked(content, chunkSize):
            chunkEncoded = b64encode(chunk).decode()

            self.__dbxApi.dbfs.add_block(handle, chunkEncoded)

        self.__dbxApi.dbfs.close(handle)

    def __chunked(self, source, size):
        for i in range(0, len(source), size):
            yield source[i:i+size]
