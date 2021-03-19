import json
from zipfile import ZipInfo, ZipFile
from dbxdeploy.notebook.converter.DatabricksNotebookConverter import DatabricksNotebookConverter


class DbcNotebookConverter:
    def __init__(
        self,
        databricks_notebook_converter: DatabricksNotebookConverter,
    ):
        self.__databricks_notebook_converter = databricks_notebook_converter

    def convert(self, zip_file: ZipFile, file: ZipInfo):
        zipped_file_content = zip_file.read(file.orig_filename).decode("utf-8")
        py_content = self.__databricks_notebook_converter.from_dbc_notebook(json.loads(zipped_file_content))

        return py_content.encode("utf-8")
