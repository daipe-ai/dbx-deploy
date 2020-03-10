import re
from pathlib import Path, PurePosixPath
from dbxdeploy.notebook.LibsRunPreparer import LibsRunPreparer
from dbxdeploy.notebook.converter.CellsExtractor import CellsExtractor
from dbxdeploy.notebook.converter.DbcScriptRenderer import DbcScriptRenderer
from dbxdeploy.notebook.converter.JinjaTemplateLoader import JinjaTemplateLoader
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface

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

    def toDbcNotebook(self, notebookPath: Path, whlFilename: PurePosixPath) -> str:
        originalScript = self.__loadNotebook(notebookPath)

        libsRunCell = {
            'source': self.__libsRunPreparer.prepare(whlFilename),
            'cell_type': 'code',
        }

        cells = [libsRunCell] + self.__cellsExtractor.extract(originalScript, r'#%%\n+')
        template = self.__jinjaTemplateLoader.load()

        return self.__dbcScriptRenderer.render(notebookPath, template, cells)

    def toWorkspaceImportNotebook(self, notebookPath: Path, whlFilename: PurePosixPath) -> str:
        script = self.__loadNotebook(notebookPath)

        script = (
            '# Databricks notebook source\n\n' +
            self.__libsRunPreparer.prepare(whlFilename) + '\n\n' +
            script
        )

        cellSeparatorRegex = re.compile(r'^#%%', re.MULTILINE)
        script = re.sub(cellSeparatorRegex, '# COMMAND ----------', script)

        return script

    def resolves(self, fileExtension: str) -> bool:
        return fileExtension == 'py'

    def getGlobPatterns(self) -> list:
        return self.__consumerGlobs + self.__jobGlobs

    def getConsumerGlobPatterns(self) -> list:
        return self.__consumerGlobs

    def getDescription(self):
        return 'Python consumers and jobs'

    def __loadNotebook(self, notebookPath: Path):
        with notebookPath.open('r', encoding='utf-8') as f:
            return f.read()
