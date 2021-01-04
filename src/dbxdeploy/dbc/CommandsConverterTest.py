import unittest
from pyfonycore.bootstrap import bootstrappedContainer
from dbxdeploy.dbc.CommandConverter import CommandConverter
from dbxdeploy.dbc.CommandsConverter import CommandsConverter
from dbxdeploy.notebook.converter.DatabricksNotebookConverter import DatabricksNotebookConverter

class CommandsConverterTest(unittest.TestCase):

    def setUp(self):
        container = bootstrappedContainer.init('test')
        self.__commandConverter = container.get(CommandConverter) # type: CommandConverter

    def test_forcedEndFileNewLine(self):
        result = self.__createResult(True)

        self.__assertNotebook([
            '# Databricks notebook source',
            '# MAGIC %run /foo/bar',
            '',
            '# COMMAND ----------',
            '',
            'print("Hello world")',
            '',
        ], result)

    def test_noForcedEndFileNewLine(self):
        result = self.__createResult(False)

        self.__assertNotebook([
            '# Databricks notebook source',
            '# MAGIC %run /foo/bar',
            '',
            '# COMMAND ----------',
            '',
            'print("Hello world")',
        ], result)

    def __createResult(self, forceEndFileNewLine: bool):
        commandsConverter = CommandsConverter(forceEndFileNewLine, self.__commandConverter) # type: CommandsConverter

        commands = [
            {'command': 'print("Hello world")', 'position': 2, 'commandTitle': ''},
            {'command': '%run /foo/bar', 'position': 1, 'commandTitle': ''},
            {'command': '', 'position': 1.33, 'commandTitle': ''},
            {'command': '', 'position': 1.66, 'commandTitle': ''}
        ]

        return commandsConverter.convert(
            commands,
            DatabricksNotebookConverter.firstLine,
            DatabricksNotebookConverter.cellSeparator,
        )

    def __assertNotebook(self, expected: list, resultCode: str):
        resultLines = resultCode.split('\n')

        self.assertEqual(expected, resultLines)

if __name__ == '__main__':
    unittest.main()
