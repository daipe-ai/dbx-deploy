from pathlib import Path, PurePosixPath
from dbxdeploy.notebook.converter.CellsExtractor import CellsExtractor
from dbxdeploy.notebook.converter.DbcScriptRenderer import DbcScriptRenderer
from dbxdeploy.notebook.converter.JinjaTemplateLoader import JinjaTemplateLoader
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface

class DatabricksNotebookConverter(NotebookConverterInterface):

    def __init__(
        self,
        notebookGlobs: list,
        cellsExtractor: CellsExtractor,
        jinjaTemplateLoader: JinjaTemplateLoader,
        dbcScriptRenderer: DbcScriptRenderer,
    ):
        self.__notebookGlobs = notebookGlobs
        self.__cellsExtractor = cellsExtractor
        self.__jinjaTemplateLoader = jinjaTemplateLoader
        self.__dbcScriptRenderer = dbcScriptRenderer

    def toDbcNotebook(self, notebookPath: Path, whlFilename: PurePosixPath) -> str:
        originalScript = self.__loadNotebook(notebookPath)
        cells = self.__cellsExtractor.extract(originalScript, r'#[\s]+COMMAND[\s]+[\-]+\n+')
        template = self.__jinjaTemplateLoader.load()

        return self.__dbcScriptRenderer.render(notebookPath, template, cells, whlFilename)

    def toWorkspaceImportNotebook(self, notebookPath: Path, whlFilename: PurePosixPath) -> str:
        return self.__loadNotebook(notebookPath)

    def resolves(self, fileExtension: str) -> bool:
        return fileExtension == 'py'

    def getGlobPatterns(self) -> list:
        return self.__notebookGlobs

    def getConsumerGlobPatterns(self) -> list:
        return []

    def getDescription(self):
        return 'Databricks notebooks'

    def __loadNotebook(self, notebookPath: Path):
        with notebookPath.open() as f:
            return f.read()
