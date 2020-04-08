import unittest
from dbxdeploy.containerInit import initContainer
from dbxdeploy.dbc.NotebookConverter import NotebookConverter
from dbxdeploy.notebook.converter.DatabricksNotebookConverter import DatabricksNotebookConverter

class NotebookConverterTest(unittest.TestCase):

    def setUp(self):
        container = initContainer('test')

        self.__notebookConverter = container.get(NotebookConverter) # type: NotebookConverter

    def test_basic(self):
        commands = [
            {'command': 'print("Hello world")', 'position': 2, 'commandTitle': ''},
            {'command': '%run /foo/bar', 'position': 1, 'commandTitle': ''},
            {'command': '', 'position': 1.33, 'commandTitle': ''},
            {'command': '', 'position': 1.66, 'commandTitle': ''}
        ]

        result = self.__notebookConverter.convert(
            commands,
            DatabricksNotebookConverter.firstLine,
            DatabricksNotebookConverter.cellSeparator,
        )

        self.assertNotebook([
            '# Databricks notebook source',
            '# MAGIC %run /foo/bar',
            '',
            '# COMMAND ----------',
            '',
            'print("Hello world")',
            '',
        ], result)

    def assertNotebook(self, expected: list, resultCode: str):
        resultLines = resultCode.split('\n')

        self.assertEqual(expected, resultLines)

if __name__ == '__main__':
    unittest.main()
