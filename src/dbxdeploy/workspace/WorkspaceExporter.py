from requests.exceptions import HTTPError
from dbxdeploy.utils.DatabricksClient import DatabricksClient
from pathlib import PurePosixPath
import base64
from dbxdeploy.workspace.WorkspaceExportException import WorkspaceExportException


class WorkspaceExporter:
    def __init__(self, dbx_api: DatabricksClient):
        self.__dbx_api = dbx_api

    def export(self, path: PurePosixPath) -> bytes:
        try:
            response = self.__dbx_api.workspace.export_workspace(str(path), format="DBC")
        except HTTPError:
            raise WorkspaceExportException()

        return base64.decodebytes(response["content"].encode("utf-8"))
