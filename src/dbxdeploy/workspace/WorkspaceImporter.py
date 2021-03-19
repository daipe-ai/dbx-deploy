from base64 import b64encode
from pathlib import PurePosixPath
from databricks_api import DatabricksAPI
import os


class WorkspaceImporter:
    def __init__(
        self,
        dbx_api: DatabricksAPI,
    ):
        self.__dbx_api = dbx_api

    def overwrite_script(self, script: str, target_path: PurePosixPath):
        content_to_upload = b64encode(script.encode("utf-8"))

        self.__dbx_api.workspace.mkdirs(os.path.dirname(str(target_path)))

        self.__dbx_api.workspace.import_workspace(
            str(target_path), format="SOURCE", language="PYTHON", content=str(content_to_upload, "utf-8"), overwrite=True
        )
