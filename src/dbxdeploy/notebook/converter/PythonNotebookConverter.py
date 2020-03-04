import re
from pathlib import Path, PurePosixPath
from typing import List
from dbxdeploy.notebook.LibsRunPreparer import LibsRunPreparer
from dbxdeploy.notebook.converter.DbcScriptRenderer import DbcScriptRenderer
from dbxdeploy.notebook.converter.JinjaTemplateLoader import JinjaTemplateLoader
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface

class PythonNotebookConverter(NotebookConverterInterface):

    def __init__(
        self,
        consumerGlobs: list,
        jobGlobs: list,
        libsRunPreparer: LibsRunPreparer,
        jinjaTemplateLoader: JinjaTemplateLoader,
        dbcScriptRenderer: DbcScriptRenderer,
    ):
        self.__consumerGlobs = consumerGlobs
        self.__jobGlobs = jobGlobs
        self.__libsRunPreparer = libsRunPreparer
        self.__jinjaTemplateLoader = jinjaTemplateLoader
        self.__dbcScriptRenderer = dbcScriptRenderer

    def toDbcNotebook(self, notebookPath: Path, whlFilename: PurePosixPath) -> str:
        originalScript = self.__loadNotebook(notebookPath)
        cells = self.__extractCells(originalScript)
        template = self.__jinjaTemplateLoader.load()

        return self.__dbcScriptRenderer.render(notebookPath, template, cells, whlFilename)

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

    def __extractCells(self, originalScript: str) -> List[dict]:
        def removeEndingSpaces(cell: str):
            return re.sub(r'\n+$', '', cell)

        rawCells = re.split(r'#%%\n+', originalScript)
        rawCells = list(filter(lambda rawCell: rawCell != '', rawCells))
        rawCells = list(map(removeEndingSpaces, rawCells))

        return list(map(lambda rawCell: {'source': rawCell, 'cell_type': 'code'}, rawCells))

    def __loadNotebook(self, notebookPath: Path):
        with notebookPath.open() as f:
            return f.read()
