import re
from pathlib import PurePosixPath
from dbxdeploy.dbc.NotebookConverter import NotebookConverter
from dbxdeploy.notebook.converter.CellsExtractor import CellsExtractor
from dbxdeploy.notebook.converter.DbcScriptRenderer import DbcScriptRenderer
from dbxdeploy.notebook.converter.JinjaTemplateLoader import JinjaTemplateLoader
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException

class DatabricksNotebookConverter:

    firstLine = '# Databricks notebook source'

    def __init__(
        self,
        whlBaseDir: str,
        notebookConverter: NotebookConverter,
        cellsExtractor: CellsExtractor,
        jinjaTemplateLoader: JinjaTemplateLoader,
        dbcScriptRenderer: DbcScriptRenderer,
    ):
        self.__whlBaseDir = whlBaseDir
        self.__notebookConverter = notebookConverter
        self.__cellsExtractor = cellsExtractor
        self.__jinjaTemplateLoader = jinjaTemplateLoader
        self.__dbcScriptRenderer = dbcScriptRenderer

    def validateSource(self, source: str):
        if re.match(r'^' + self.firstLine + '[\r\n]', source) is None:
            raise UnexpectedSourceException()

    def fromDbcNotebook(self, content: dict) -> str:
        def convertCommand(command: dict):
            if command['command'][0:5] == '%run ' or command['command'][0:4] == '%md ':
                return '# MAGIC ' + command['command']

            if command['commandTitle']:
                return '# DBTITLE 1,' + command['commandTitle'] + '\n' + command['command']

            regExp = (
                '^' + re.escape('dbutils.library.install(\'' + self.__whlBaseDir) +
                '/[^/]+/[\\d]{4}-[\\d]{2}-[\\d]{2}_[\\d]{2}-[\\d]{2}-[\\d]{2}_[\\w]+/[^-]+-[\\d.]+-py3-none-any.whl\'\\)$'
            )

            if re.match(regExp, command['command']):
                return '# MAGIC %installMasterPackageWhl'

            return command['command']

        return self.__notebookConverter.convert(
            content['commands'],
            convertCommand,
            self.firstLine,
            '# COMMAND ----------'
        )

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
