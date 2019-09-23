from base64 import b64encode
from databricks_api import DatabricksAPI
from DbxDeploy.Setup.Version.VersionInterface import VersionInterface
from requests.exceptions import HTTPError

class DbcUploader:

    def __init__(self, dbxProjectRoot: str, dbxApi: DatabricksAPI):
        self.__dbxProjectRoot = dbxProjectRoot
        self.__dbxApi = dbxApi

    def upload(self, dbcContent: bytes, version: VersionInterface):
        contentToUpload = b64encode(dbcContent).decode()

        self.__dbxApi.workspace.import_workspace(
            version.getDbxVersionPath(self.__dbxProjectRoot),
            format='DBC',
            content=contentToUpload
        )

        try:
            self.__dbxApi.workspace.delete(
                self.__dbxProjectRoot + '/_current',
                recursive=True,
            )
        except HTTPError:
            pass

        self.__dbxApi.workspace.import_workspace(
            self.__dbxProjectRoot + '/_current',
            format='DBC',
            content=contentToUpload
        )
