import os
from dbxdeploy.dbc.CommandConverter import CommandConverter


class CommandsConverter:
    def __init__(self, force_end_file_newline: bool, black_enabled: bool, command_converter: CommandConverter):
        self.__force_end_file_newline = force_end_file_newline
        self.__black_enabled = black_enabled
        self.__command_converter = command_converter

    def convert(self, commands: list, first_line: str, cell_separator: str) -> str:
        while commands[len(commands) - 1]["command"] == "":
            commands.pop()

        commands.sort(key=lambda command: command["position"])
        commands = list(map(self.__command_converter.convert, commands))

        output = f"\n\n{cell_separator}\n\n".join(commands)

        return self.__format(first_line, output)

    def __format(self, first_line: str, output: str):

        if self.__black_enabled:
            try:
                import black

                black_config = black.parse_pyproject_toml(os.getcwd() + "/pyproject.toml")
                black_mode = black.Mode(**black_config)

                return black.format_str(first_line + "\n" + output, mode=black_mode)
            except ImportError:
                raise Exception("Black enabled but not installed")
        else:
            if self.__force_end_file_newline is True and output[-1:] != "\n":
                output += "\n"

            return first_line + "\n" + output
