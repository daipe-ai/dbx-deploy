import re
from pathlib import Path, PurePosixPath
from dbxdeploy.notebook.LibsRunPreparer import LibsRunPreparer
from dbxdeploy.notebook.converter.CellsExtractor import CellsExtractor
from dbxdeploy.notebook.converter.DbcScriptRenderer import DbcScriptRenderer
from dbxdeploy.notebook.converter.JinjaTemplateLoader import JinjaTemplateLoader
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException

class PythonNotebookConverter(NotebookConverterInterface):

    def __init__(
        self,
        consumerGlobs: list,
        jobGlobs: list,
        libsRunPreparer: LibsRunPreparer,
        cellsExtractor: CellsExtractor,
        jinjaTemplateLoader: JinjaTemplateLoader,
        dbcScriptRenderer: DbcScriptRenderer,
    ):
        self.__consumerGlobs = consumerGlobs
        self.__jobGlobs = jobGlobs
        self.__libsRunPreparer = libsRunPreparer
        self.__cellsExtractor = cellsExtractor
        self.__jinjaTemplateLoader = jinjaTemplateLoader
        self.__dbcScriptRenderer = dbcScriptRenderer

    def getSupportedExtensions(self) -> list:
        return ['py']

    def loadSource(self, notebookPath: Path) -> str:
        with notebookPath.open('r', encoding='utf-8') as f:
            source = f.read()

        if re.match(r'^#%%[\r\n]', source) is None:
            raise UnexpectedSourceException()

        return source

    def toDbcNotebook(self, notebookName: str, source: str, whlFilename: PurePosixPath) -> str:
        libsRunCell = {
            'source': self.__libsRunPreparer.prepare(whlFilename),
            'cell_type': 'code',
        }

        cells = [libsRunCell] + self.__cellsExtractor.extract(source, r'#%%\n+')
        template = self.__jinjaTemplateLoader.load()

        return self.__dbcScriptRenderer.render(notebookName, template, cells)

    def toWorkspaceImportNotebook(self, source: str, whlFilename: PurePosixPath) -> str:
        script = (
            '# Databricks notebook source\n\n' +
            self.__libsRunPreparer.prepare(whlFilename) + '\n\n' +
            source
        )

        cellSeparatorRegex = re.compile(r'^#%%', re.MULTILINE)
        script = re.sub(cellSeparatorRegex, '# COMMAND ----------', script)

        return script

    def getGlobPatterns(self) -> list:
        return self.__consumerGlobs + self.__jobGlobs

    def getConsumerGlobPatterns(self) -> list:
        return self.__consumerGlobs

    def getDescription(self):
        return 'Python consumers and jobs'
