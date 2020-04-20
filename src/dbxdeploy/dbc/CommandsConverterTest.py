import unittest
from dbxdeploy.containerInit import initContainer
from dbxdeploy.dbc.CommandsConverter import CommandsConverter
from dbxdeploy.notebook.converter.DatabricksNotebookConverter import DatabricksNotebookConverter

class CommandsConverterTest(unittest.TestCase):

    def setUp(self):
        container = initContainer('test')

        self.__commandsConverter = container.get(CommandsConverter) # type: CommandsConverter

    def test_basic(self):
        commands = [
            {'command': 'print("Hello world")', 'position': 2, 'commandTitle': ''},
            {'command': '%run /foo/bar', 'position': 1, 'commandTitle': ''},
            {'command': '', 'position': 1.33, 'commandTitle': ''},
            {'command': '', 'position': 1.66, 'commandTitle': ''}
        ]

        result = self.__commandsConverter.convert(
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
