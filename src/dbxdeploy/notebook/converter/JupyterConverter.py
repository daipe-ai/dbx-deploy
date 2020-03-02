from pathlib import Path, PurePosixPath
from DbxNotebookExporter.Databricks.DatabricksNotebookExporter import DatabricksNotebookExporter
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface
from DbxNotebookExporter.Json.JsonNotebookExporter import JsonNotebookExporter
from dbxdeploy.notebook.LibsRunPreparer import LibsRunPreparer

class JupyterConverter(NotebookConverterInterface):

    def __init__(
        self,
        consumerGlobs: list,
        jsonNotebookExporter: JsonNotebookExporter,
        databricksNotebookExporter: DatabricksNotebookExporter,
        libsRunPreparer: LibsRunPreparer,
    ):
        self.__consumerGlobs = consumerGlobs
        self.__jsonNotebookExporter = jsonNotebookExporter
        self.__databricksNotebookExporter = databricksNotebookExporter
        self.__libsRunPreparer = libsRunPreparer

    def toDbcNotebook(self, notebookPath: Path, whlFilename: PurePosixPath) -> str:
        resources = {'libsRun': self.__libsRunPreparer.prepare(whlFilename)}
        script, _ = self.__jsonNotebookExporter.from_filename(str(notebookPath), resources)

        return script

    def toWorkspaceImportNotebook(self, notebookPath: Path, whlFilename: PurePosixPath) -> str:
        resources = {'libsRun': self.__libsRunPreparer.prepare(whlFilename)}
        script, _ = self.__databricksNotebookExporter.from_filename(str(notebookPath), resources)

        return script

    def resolves(self, fileExtension: str) -> bool:
        return fileExtension == 'ipynb'

    def getGlobPatterns(self) -> list:
        return ['**/*.ipynb']

    def getConsumerGlobPatterns(self) -> list:
        return self.__consumerGlobs

    def getDescription(self):
        return 'Jupyter notebooks (*.ipynb)'
