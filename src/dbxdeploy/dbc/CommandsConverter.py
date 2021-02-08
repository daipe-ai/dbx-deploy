import os
from dbxdeploy.dbc.CommandConverter import CommandConverter

class CommandsConverter:

    def __init__(
        self,
        forceEndFileNewLine: bool,
        commandConverter: CommandConverter,
    ):
        self.__forceEndFileNewLine = forceEndFileNewLine
        self.__commandConverter = commandConverter

    def convert(self, commands: list, firstLine: str, cellSeparator: str) -> str:
        while commands[len(commands) - 1]['command'] == '':
            commands.pop()

        commands.sort(key=lambda command: command['position'])
        commands = list(map(self.__commandConverter.convert, commands))

        output = f'\n\n{cellSeparator}\n\n'.join(commands)

        return self.__format(firstLine, output)

    def __format(self, firstLine: str, output: str):
        try:
            import black # pylint: disable = import-outside-toplevel

            blackConfig = black.parse_pyproject_toml(os.getcwd() + '/pyproject.toml')
            blackMode = black.Mode(**blackConfig)

            return black.format_str(firstLine + '\n' + output, mode=blackMode)
        except ImportError:
            if self.__forceEndFileNewLine is True and output[-1:] != '\n':
                output += '\n'

            return firstLine + '\n' + output
