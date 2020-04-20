import re
from pathlib import PurePosixPath
from dbxdeploy.dbc.CommandsConverter import CommandsConverter
from dbxdeploy.notebook.converter.CellsExtractor import CellsExtractor
from dbxdeploy.notebook.converter.DbcScriptRenderer import DbcScriptRenderer
from dbxdeploy.notebook.converter.JinjaTemplateLoader import JinjaTemplateLoader
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException

class DatabricksNotebookConverter:

    firstLine = '# Databricks notebook source'
    cellSeparator = '# COMMAND ----------'

    def __init__(
        self,
        commandsConverter: CommandsConverter,
        cellsExtractor: CellsExtractor,
        jinjaTemplateLoader: JinjaTemplateLoader,
        dbcScriptRenderer: DbcScriptRenderer,
    ):
        self.__commandsConverter = commandsConverter
        self.__cellsExtractor = cellsExtractor
        self.__jinjaTemplateLoader = jinjaTemplateLoader
        self.__dbcScriptRenderer = dbcScriptRenderer

    def validateSource(self, source: str):
        if re.match(r'^' + self.firstLine + '[\r\n]', source) is None:
            raise UnexpectedSourceException()

    def fromDbcNotebook(self, content: dict) -> str:
        return self.__commandsConverter.convert(content['commands'], self.firstLine, self.cellSeparator)

    def toDbcNotebook(self, notebookName: str, source: str, whlFilename: PurePosixPath) -> str:
        cells = self.__cellsExtractor.extract(source, r'#[\s]+COMMAND[\s]+[\-]+\n+')

        def cleanupCell(cell: dict):
            if cell['source'] == '# MAGIC %installMasterPackageWhl':
                cell['source'] = self.__getMasterPackageInstallCommand(whlFilename)

            cell['source'] = re.sub(r'^' + self.firstLine + '[\r\n]+', '', cell['source'])
            cell['source'] = re.sub(r'^# MAGIC ', '', cell['source'])

            return cell

        cells = list(map(cleanupCell, cells))

        template = self.__jinjaTemplateLoader.load()

        return self.__dbcScriptRenderer.render(notebookName, template, cells)

    def toWorkspaceImportNotebook(self, source: str, whlFilename: PurePosixPath) -> str:
        return source.replace('# MAGIC %installMasterPackageWhl', self.__getMasterPackageInstallCommand(whlFilename))

    def __getMasterPackageInstallCommand(self, whlFilename: PurePosixPath):
        return 'dbutils.library.install(\'{}\')'.format(whlFilename)
