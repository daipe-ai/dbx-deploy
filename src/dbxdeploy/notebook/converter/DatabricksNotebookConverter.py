import re
from pathlib import Path, PurePosixPath
from dbxdeploy.notebook.converter.CellsExtractor import CellsExtractor
from dbxdeploy.notebook.converter.DbcScriptRenderer import DbcScriptRenderer
from dbxdeploy.notebook.converter.JinjaTemplateLoader import JinjaTemplateLoader
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException

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

    def getSupportedExtensions(self) -> list:
        return ['py']

    def loadSource(self, notebookPath: Path) -> str:
        with notebookPath.open('r', encoding='utf-8') as f:
            source = f.read()

        if re.match(r'^# Databricks notebook source[\r\n]', source) is None:
            raise UnexpectedSourceException()

        return source

    def toDbcNotebook(self, notebookName: str, source: str, whlFilename: PurePosixPath) -> str:
        cells = self.__cellsExtractor.extract(source, r'#[\s]+COMMAND[\s]+[\-]+\n+')

        def cleanupCell(cell: dict):
            cell['source'] = re.sub(r'^# Databricks notebook source[\r\n]+', '', cell['source'])
            cell['source'] = re.sub(r'^# MAGIC ', '', cell['source'])

            return cell

        cells = list(map(cleanupCell, cells))

        template = self.__jinjaTemplateLoader.load()

        return self.__dbcScriptRenderer.render(notebookName, template, cells)

    def toWorkspaceImportNotebook(self, source: str, whlFilename: PurePosixPath) -> str:
        return source

    def getGlobPatterns(self) -> list:
        return self.__notebookGlobs

    def getConsumerGlobPatterns(self) -> list:
        return []

    def getDescription(self):
        return 'Databricks notebooks'
