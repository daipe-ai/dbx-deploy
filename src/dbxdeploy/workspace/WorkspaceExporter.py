from typing import List
from databricks_api import DatabricksAPI
from pathlib import PurePosixPath
from dbxdeploy.workspace.PathNotExistException import PathNotExistException
from requests.exceptions import HTTPError
from io import BytesIO
import zipfile
import base64

class WorkspaceExporter:

    def __init__(self, dbxApi: DatabricksAPI):
        self.__dbxApi = dbxApi

    def export(self, path: PurePosixPath) -> List[str]:
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
                """
                _current/myproject/foo/bar.python -> myproject/foo/bar.python (releases enabled)
                mybranch/myproject/foo/bar.python -> myproject/foo/bar.python (releases disabled)
                """
                filePathWithoutRootdir = file.orig_filename[file.orig_filename.index('/') + 1:]

                fileNames.append(filePathWithoutRootdir)

        zipFile.close()
        buffer.seek(0)

        return fileNames
