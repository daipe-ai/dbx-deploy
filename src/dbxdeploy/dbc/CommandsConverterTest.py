import unittest
from pyfonycore.bootstrap import bootstrapped_container
from dbxdeploy.dbc.CommandConverter import CommandConverter
from dbxdeploy.dbc.CommandsConverter import CommandsConverter
from dbxdeploy.notebook.converter.CommandSeparatorConverter import CommandSeparatorConverter
from dbxdeploy.black.BlackChecker import BlackChecker
from logging import Logger


class CommandsConverterTest(unittest.TestCase):
    def setUp(self):
        container = bootstrapped_container.init("test")
        self.__logger = Logger("test")
        self.__command_converter = container.get(CommandConverter)  # type: CommandConverter

    def test_forced_end_file_new_line(self):
        result = self.__create_result(True, False)

        self.__assert_notebook(
            [
                "# Databricks notebook source",
                "# MAGIC %run /foo/bar",
                "",
                "# COMMAND ----------",
                "",
                'print("Hello world")',
                "",
            ],
            result,
        )

    def test_no_forced_end_file_new_line(self):
        result = self.__create_result(False, False)

        self.__assert_notebook(
            [
                "# Databricks notebook source",
                "# MAGIC %run /foo/bar",
                "",
                "# COMMAND ----------",
                "",
                'print("Hello world")',
            ],
            result,
        )

    def __create_result(self, force_end_file_newline: bool, black_enabled: bool):
        commands_converter = CommandsConverter(
            force_end_file_newline, self.__logger, self.__command_converter, BlackChecker(black_enabled)
        )  # type: CommandsConverter

        commands = [
            {"command": 'print("Hello world")', "position": 2, "commandTitle": "", "subtype": "command"},
            {"command": "%run /foo/bar", "position": 1, "commandTitle": "", "subtype": "command"},
            {"command": "", "position": 1.33, "commandTitle": "", "subtype": "command"},
            {"command": "", "position": 1.66, "commandTitle": "", "subtype": "command"},
        ]

        return commands_converter.convert(
            commands,
            CommandSeparatorConverter.first_line,
            CommandSeparatorConverter.cell_separator,
        )

    def __assert_notebook(self, expected: list, result_code: str):
        result_lines = result_code.split("\n")

        self.assertEqual(expected, result_lines)


if __name__ == "__main__":
    unittest.main()
