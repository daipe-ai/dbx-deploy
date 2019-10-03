from base64 import b64encode
from pathlib import PurePosixPath
from databricks_api import DatabricksAPI
from requests.exceptions import HTTPError

class DbcUploader:

    def __init__(
        self,
        dbxApi: DatabricksAPI
    ):
        self.__dbxApi = dbxApi

    def upload(self, dbcContent: bytes, releasePath: PurePosixPath):
        contentToUpload = b64encode(dbcContent).decode()

        try:
            self.__performUpload(contentToUpload, releasePath)
        except HTTPError:
            self.__dbxApi.workspace.mkdirs(str(releasePath.parent))
            self.__performUpload(contentToUpload, releasePath)

    def __performUpload(self, contentToUpload, releasePath: PurePosixPath):
        self.__dbxApi.workspace.import_workspace(
            str(releasePath),
            format='DBC',
            content=contentToUpload,
        )
