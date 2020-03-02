from pathlib import Path, PurePosixPath
from typing import List
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface
from DbxNotebookExporter.Json.formatCellContent import formatCellContent
from dbxdeploy.notebook.LibsRunPreparer import LibsRunPreparer
import DbxNotebookExporter.Json.JsonNotebookExporter as JsonNotebookExporterModule
import nbconvert.templates.skeleton as nbConvertSkeleton
import jinja2
import re
import os

class PythonNotebookConverter(NotebookConverterInterface):

    def __init__(
        self,
        consumerGlobs: list,
        jobGlobs: list,
        libsRunPreparer: LibsRunPreparer,
    ):
        self.__consumerGlobs = consumerGlobs
        self.__jobGlobs = jobGlobs
        self.__libsRunPreparer = libsRunPreparer

    def toDbcNotebook(self, notebookPath: Path, whlFilename: PurePosixPath) -> str:
        originalScript = self.__loadNotebook(notebookPath)
        cells = self.__extractCells(originalScript)
        template = self.__loadJinjaTemplate()

        script = template.render(
            resources={
                'libsRun': self.__libsRunPreparer.prepare(whlFilename),
                'metadata': {
                    'name': notebookPath.stem
                },
                'global_content_filter': {
                    'include_code': True,
                    'include_input': False,
                    'include_input_prompt': False,
                    'include_output': False,
                }
            },
            nb={'cells': cells}
        )

        return script

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

    def __loadJinjaTemplate(self):
        basePaths = [
            os.path.dirname(JsonNotebookExporterModule.__file__),
            nbConvertSkeleton.__path__._path[0] # pylint: disable = no-member, protected-access
        ]

        templateLoader = jinja2.FileSystemLoader(searchpath=basePaths)
        templateEnv = jinja2.Environment(loader=templateLoader)
        templateEnv.filters['formatCellContent'] = formatCellContent

        return templateEnv.get_template('json_notebook.tpl')
