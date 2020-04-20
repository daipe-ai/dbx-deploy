from dbxdeploy.dbc.CommandConverter import CommandConverter

class CommandsConverter:

    def __init__(
        self,
        commandConverter: CommandConverter,
    ):
        self.__commandConverter = commandConverter

    def convert(self, commands: list, firstLine: str, cellSeparator: str) -> str:
        while commands[len(commands) - 1]['command'] == '':
            commands.pop()

        commands.sort(key=lambda command: command['position'])
        commands = list(map(self.__commandConverter.convert, commands))

        output = f'\n\n{cellSeparator}\n\n'.join(commands)

        if output[-1:] != '\n':
            output += '\n'

        return firstLine + '\n' + output
