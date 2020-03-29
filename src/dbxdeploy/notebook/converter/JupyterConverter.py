from pathlib import Path, PurePosixPath
import nbformat
from dbxnotebookexporter.databricks.DatabricksNotebookExporter import DatabricksNotebookExporter
from nbconvert.exporters.exporter import ResourcesDict
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface
from dbxnotebookexporter.json.JsonNotebookExporter import JsonNotebookExporter
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

    def getSupportedExtensions(self) -> list:
        return ['ipynb']

    def loadSource(self, notebookPath: Path) -> str:
        with notebookPath.open('r', encoding='utf-8') as f:
            return f.read()

    def toDbcNotebook(self, notebookName: str, source: str, whlFilename: PurePosixPath) -> str:
        nbSource = nbformat.reads(source, as_version=4)
        resources = self.__prepareResources(whlFilename)
        resources['metadata']['name'] = notebookName
        script, _ = self.__jsonNotebookExporter.from_notebook_node(nbSource, resources=resources)

        return script

    def toWorkspaceImportNotebook(self, source: str, whlFilename: PurePosixPath) -> str:
        nbSource = nbformat.reads(source, as_version=4)
        script, _ = self.__databricksNotebookExporter.from_notebook_node(nbSource, resources=self.__prepareResources(whlFilename))

        return script

    def getGlobPatterns(self) -> list:
        return ['**/*.ipynb']

    def getConsumerGlobPatterns(self) -> list:
        return self.__consumerGlobs

    def getDescription(self):
        return 'Jupyter notebooks (*.ipynb)'

    def __prepareResources(self, whlFilename: PurePosixPath):
        resources = ResourcesDict()
        resources['metadata'] = ResourcesDict()
        resources['libsRun'] = self.__libsRunPreparer.prepare(whlFilename)

        return resources
