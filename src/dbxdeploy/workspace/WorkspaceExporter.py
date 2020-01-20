from typing import List
from databricks_api import DatabricksAPI
from pathlib import PurePosixPath
from dbxdeploy.workspace.PathNotExistException import PathNotExistException
from requests.exceptions import HTTPError
from io import BytesIO
import zipfile
import base64

class WorkspaceExporter:

    def __init__(self, dbxApi: DatabricksAPI) -> List[str]:
        self.__dbxApi = dbxApi

    def export(self, path: PurePosixPath):
        try:
            response = self.__dbxApi.workspace.export_workspace(str(path), format='DBC')
        except HTTPError:
            raise PathNotExistException()

        binaryContent = base64.decodebytes(response['content'].encode('utf-8'))

        buffer = BytesIO()
        buffer.write(binaryContent)

        zipFile = zipfile.ZipFile(buffer, 'r', zipfile.ZIP_DEFLATED)

        fileNames = []

        for file in zipFile.filelist:
            if file.orig_filename[-1:] != '/':
                fileNames.append(file.orig_filename)

        zipFile.close()
        buffer.seek(0)

        return fileNames
