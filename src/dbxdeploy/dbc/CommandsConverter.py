import os
from dbxdeploy.dbc.CommandConverter import CommandConverter
from dbxdeploy.black.BlackChecker import BlackChecker
from logging import Logger


class CommandsConverter:
    def __init__(self, force_end_file_newline: bool, logger: Logger, command_converter: CommandConverter, black_checker: BlackChecker):
        self.__force_end_file_newline = force_end_file_newline
        self.__logger = logger
        self.__command_converter = command_converter
        self.__black_checker = black_checker

    def convert(self, commands: list, first_line: str, cell_separator: str) -> str:
        while commands[len(commands) - 1]["command"] == "":
            commands.pop()

        commands.sort(key=lambda command: command["position"])
        commands = [command for command in commands if command["subtype"] == "command"]
        commands = list(map(self.__command_converter.convert, commands))

        output = f"\n\n{cell_separator}\n\n".join(commands)

        return self.__format(first_line, output)

    def __format(self, first_line: str, output: str):
        def format_without_black(starting_line: str, text: str):
            if self.__force_end_file_newline and text[-1:] != "\n":
                text += "\n"

            return starting_line + "\n" + text

        if self.__black_checker.is_black_enabled and self.__black_checker.is_black_installed:
            import black

            black_config = black.parse_pyproject_toml(os.getcwd() + "/pyproject.toml")
            black_mode = black.Mode(**black_config)

            return black.format_str(first_line + "\n" + output, mode=black_mode)

        else:
            return format_without_black(first_line, output)
