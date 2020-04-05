# pylint: disable = too-many-instance-attributes
import re
from pathlib import PurePosixPath
from dbxdeploy.dbc.NotebookConverter import NotebookConverter
from dbxdeploy.notebook.LibsRunPreparer import LibsRunPreparer
from dbxdeploy.notebook.converter.CellsExtractor import CellsExtractor
from dbxdeploy.notebook.converter.DbcScriptRenderer import DbcScriptRenderer
from dbxdeploy.notebook.converter.JinjaTemplateLoader import JinjaTemplateLoader
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException

class PythonNotebookConverter(NotebookConverterInterface):

    def __init__(
        self,
        whlBaseDir: str,
        consumerGlobs: list,
        jobGlobs: list,
        notebookConverter: NotebookConverter,
        libsRunPreparer: LibsRunPreparer,
        cellsExtractor: CellsExtractor,
        jinjaTemplateLoader: JinjaTemplateLoader,
        dbcScriptRenderer: DbcScriptRenderer,
    ):
        self.__whlBaseDir = whlBaseDir
        self.__consumerGlobs = consumerGlobs
        self.__jobGlobs = jobGlobs
        self.__notebookConverter = notebookConverter
        self.__libsRunPreparer = libsRunPreparer
        self.__cellsExtractor = cellsExtractor
        self.__jinjaTemplateLoader = jinjaTemplateLoader
        self.__dbcScriptRenderer = dbcScriptRenderer

    def getSupportedExtensions(self) -> list:
        return ['py']

    def validateSource(self, source: str):
        if re.match(r'^#%%[\r\n]', source) is None:
            raise UnexpectedSourceException()

    def fromDbcNotebook(self, content: dict) -> str:
        def convertCommand(command: dict):
            regExp = (
                '^' + re.escape('dbutils.library.install(\'' + self.__whlBaseDir) +
                '/[^/]+/[\\d]{4}-[\\d]{2}-[\\d]{2}_[\\d]{2}-[\\d]{2}-[\\d]{2}_[\\w]+/[^-]+-[\\d.]+-py3-none-any.whl\'\\)$'
            )

            if re.match(regExp, command['command']):
                return None

            return command['command']

        return self.__notebookConverter.convert(content['commands'], convertCommand, '#%%\n', '#%%')

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
        return 'Python notebooks (*.py, #%% cell separator)'
