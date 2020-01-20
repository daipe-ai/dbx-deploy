from base64 import b64encode
from pathlib import PurePosixPath
from databricks_api import DatabricksAPI
import os

class WorkspaceImporter:

    def __init__(
        self,
        dbxApi: DatabricksAPI,
    ):
        self.__dbxApi = dbxApi

    def overwriteScript(self, script: str, targetPath: PurePosixPath):
        contentToUpload = b64encode(script.encode('utf-8'))

        self.__dbxApi.workspace.mkdirs(
            os.path.dirname(str(targetPath))
        )

        self.__dbxApi.workspace.import_workspace(
            str(targetPath),
            format='SOURCE',
            language='PYTHON',
            content=str(contentToUpload, 'utf-8'),
            overwrite=True
        )
