import json
from zipfile import ZipInfo, ZipFile
from dbxdeploy.notebook.converter.DatabricksNotebookConverter import DatabricksNotebookConverter

class DbcNotebookConverter:

    def __init__(
        self,
        databricksNotebookConverter: DatabricksNotebookConverter,
    ):
        self.__databricksNotebookConverter = databricksNotebookConverter

    def convert(self, zipFile: ZipFile, file: ZipInfo):
        zippedFileContent = zipFile.read(file.orig_filename).decode('utf-8')
        pyContent = self.__databricksNotebookConverter.fromDbcNotebook(json.loads(zippedFileContent))

        return pyContent.encode('utf-8')
