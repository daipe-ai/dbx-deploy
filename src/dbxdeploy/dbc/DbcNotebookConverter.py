import json
from zipfile import ZipInfo, ZipFile
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface


class DbcNotebookConverter:
    def __init__(
        self,
        notebook_converter: NotebookConverterInterface,
    ):
        self.__notebook_converter = notebook_converter

    def convert(self, zip_file: ZipFile, file: ZipInfo):
        zipped_file_content = zip_file.read(file.orig_filename).decode("utf-8")
        py_content = self.__notebook_converter.from_dbc_notebook(json.loads(zipped_file_content))

        return py_content.encode("utf-8")
