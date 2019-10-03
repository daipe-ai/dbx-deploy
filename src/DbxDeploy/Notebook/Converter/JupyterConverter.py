from pathlib import Path, PurePosixPath
from DbxNotebookExporter.Databricks.DatabricksNotebookExporter import DatabricksNotebookExporter
from DbxDeploy.Notebook.Converter.NotebookConverterInterface import NotebookConverterInterface
from DbxNotebookExporter.Json.JsonNotebookExporter import JsonNotebookExporter

class JupyterConverter(NotebookConverterInterface):

    def __init__(
        self,
        whlBasePath: str,
        jsonNotebookExporter: JsonNotebookExporter,
        databricksNotebookExporter: DatabricksNotebookExporter,
    ):
        self.__whlBasePath = PurePosixPath(whlBasePath)
        self.__jsonNotebookExporter = jsonNotebookExporter
        self.__databricksNotebookExporter = databricksNotebookExporter

    def toDbcNotebook(self, notebookPath: Path, whlFilename: str) -> str:
        resources = self.__getResources(whlFilename)
        script, _ = self.__jsonNotebookExporter.from_filename(str(notebookPath), resources)

        return script

    def toWorkspaceImportNotebook(self, notebookPath: Path, whlFilename: str) -> str:
        resources = self.__getResources(whlFilename)
        script, _ = self.__databricksNotebookExporter.from_filename(str(notebookPath), resources)

        return script

    def __getResources(self, whlFilename: str):
        whlFilename = self.__whlBasePath.joinpath(whlFilename)

        return {'libsRun': 'dbutils.library.install(\'{}\')'.format(whlFilename)}

    def resolves(self, fileExtension: str) -> bool:
        return fileExtension == 'ipynb'
