from base64 import b64encode
from pathlib import PurePosixPath
from databricks_api import DatabricksAPI
from requests.exceptions import HTTPError


class DbcUploader:
    def __init__(self, dbx_api: DatabricksAPI):
        self.__dbx_api = dbx_api

    def upload(self, dbc_content: bytes, release_path: PurePosixPath):
        content_to_upload = b64encode(dbc_content).decode()

        try:
            self.__perform_upload(content_to_upload, release_path)
        except HTTPError:
            self.__dbx_api.workspace.mkdirs(str(release_path.parent))
            self.__perform_upload(content_to_upload, release_path)

    def __perform_upload(self, content_to_upload, release_path: PurePosixPath):
        self.__dbx_api.workspace.import_workspace(
            str(release_path),
            format="DBC",
            content=content_to_upload,
        )
