class NotebookConverter:

    def convert(self, commands: list, convertCommandCallback: callable, firstLine: str, cellSeparator: str) -> str:
        commands.sort(key=lambda command: command['position'])
        commands = list(map(convertCommandCallback, commands))
        commands = list(filter(lambda command: command is not None, commands))

        while commands[len(commands) - 1] == '':
            commands.pop()

        output = f'\n\n{cellSeparator}\n\n'.join(commands)

        if output[-1:] != '\n':
            output += '\n'

        return firstLine + '\n' + output
