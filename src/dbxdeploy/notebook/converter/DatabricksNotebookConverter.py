import re
from dbxdeploy.dbc.CommandsConverter import CommandsConverter
from dbxdeploy.notebook.converter.CellsExtractor import CellsExtractor
from dbxdeploy.notebook.converter.DbcScriptRenderer import DbcScriptRenderer
from dbxdeploy.notebook.converter.JinjaTemplateLoader import JinjaTemplateLoader
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException
from dbxdeploy.package.PackageInstaller import PackageInstaller

class DatabricksNotebookConverter:

    firstLine = '# Databricks notebook source'
    cellSeparator = '# COMMAND ----------'

    def __init__(
        self,
        commandsConverter: CommandsConverter,
        cellsExtractor: CellsExtractor,
        jinjaTemplateLoader: JinjaTemplateLoader,
        dbcScriptRenderer: DbcScriptRenderer,
        packageInstaller: PackageInstaller,
    ):
        self.__commandsConverter = commandsConverter
        self.__cellsExtractor = cellsExtractor
        self.__jinjaTemplateLoader = jinjaTemplateLoader
        self.__dbcScriptRenderer = dbcScriptRenderer
        self.__packageInstaller = packageInstaller

    def validateSource(self, source: str):
        if re.match(r'^' + self.firstLine + '[\r\n]', source) is None:
            raise UnexpectedSourceException()

    def fromDbcNotebook(self, content: dict) -> str:
        return self.__commandsConverter.convert(content['commands'], self.firstLine, self.cellSeparator)

    def toDbcNotebook(self, notebookName: str, source: str, packageFilePath: str) -> str:
        cells = self.__cellsExtractor.extract(source, r'#[\s]+COMMAND[\s]+[\-]+\n+')

        def cleanupCell(cell: dict):
            if cell['source'] == '# MAGIC %installMasterPackageWhl':
                cell['source'] = self.__packageInstaller.getPackageInstallCommand(packageFilePath)

            cell['source'] = re.sub(r'^' + self.firstLine + '[\r\n]+', '', cell['source'])
            cell['source'] = re.sub(r'^# MAGIC ', '', cell['source'])

            return cell

        cells = list(map(cleanupCell, cells))

        template = self.__jinjaTemplateLoader.load()

        return self.__dbcScriptRenderer.render(notebookName, template, cells)

    def toWorkspaceImportNotebook(self, source: str, packageFilePath: str) -> str:
        return source.replace('# MAGIC %installMasterPackageWhl', self.__packageInstaller.getPackageInstallCommand(packageFilePath))
