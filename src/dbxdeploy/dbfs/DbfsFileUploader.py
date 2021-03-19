from base64 import b64encode
from databricks_api import DatabricksAPI
from dbxdeploy.package.PackageUploaderInterface import PackageUploaderInterface
from requests.exceptions import HTTPError


class DbfsFileUploader(PackageUploaderInterface):
    def __init__(self, dbx_api: DatabricksAPI):
        self.__dbx_api = dbx_api

    def upload(self, content: bytes, file_path: str, overwrite: bool = False):
        self.__streaming_upload(content, file_path, overwrite)

    def exists(self, file_path: str):
        try:
            self.__dbx_api.dbfs.get_status(file_path)

        except HTTPError as ex:
            if ex.response.status_code != 404:
                raise

            return False

        return True

    def __streaming_upload(self, content: bytes, file_path: str, overwrite: bool = False):
        response = self.__dbx_api.dbfs.create(file_path, overwrite=overwrite)
        handle = response["handle"]

        chunk_size = int(0.5 * 1024 * 1024)  # 0.5MiB

        for chunk in self.__chunked(content, chunk_size):
            chunk_encoded = b64encode(chunk).decode()

            self.__dbx_api.dbfs.add_block(handle, chunk_encoded)

        self.__dbx_api.dbfs.close(handle)

    def __chunked(self, source, size):
        for i in range(0, len(source), size):
            yield source[i : i + size]  # noqa: 5203
