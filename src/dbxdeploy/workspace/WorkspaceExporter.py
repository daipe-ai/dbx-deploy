from requests.exceptions import HTTPError
from databricks_api import DatabricksAPI
from pathlib import PurePosixPath
import base64
from dbxdeploy.workspace.WorkspaceExportException import WorkspaceExportException

class WorkspaceExporter:

    def __init__(self, dbxApi: DatabricksAPI):
        self.__dbxApi = dbxApi

    def export(self, path: PurePosixPath) -> bytes:
        try:
            response = self.__dbxApi.workspace.export_workspace(str(path), format='DBC')
        except HTTPError:
            raise WorkspaceExportException()

        return base64.decodebytes(response['content'].encode('utf-8'))
