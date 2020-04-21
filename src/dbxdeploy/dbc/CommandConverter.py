import re

class CommandConverter:

    def __init__(
        self,
        whlBaseDir: str,
    ):
        self.__whlBaseDir = whlBaseDir

    def convert(self, command: dict):
        magicCommand = self.__detectMagicCommand(command['command'])

        if magicCommand in ['%run', '%md', '%sql', '%sh', '%python', '%scala', '%r']:
            commandCode = '# MAGIC ' + command['command'].replace('\n', '\n# MAGIC ')
            return self.__processTitle(commandCode, command)

        regExp = (
            '^' + re.escape('dbutils.library.install(\'' + self.__whlBaseDir) +
            '/[^/]+/[\\d]{4}-[\\d]{2}-[\\d]{2}_[\\d]{2}-[\\d]{2}-[\\d]{2}_[\\w]+/[^-]+-[\\d.]+-py3-none-any.whl\'\\)$'
        )

        if re.match(regExp, command['command']):
            return self.__processTitle('# MAGIC %installMasterPackageWhl', command)

        return self.__processTitle(command['command'], command)

    def __detectMagicCommand(self, commandCode: str):
        matches = re.match(r'^(%[a-zA-Z]+)[\s]', commandCode)

        if not matches:
            return None

        return matches.group(1)

    def __processTitle(self, commandCode: str, origCommand: dict):
        if not origCommand['commandTitle']:
            return commandCode

        showCommandTitleString = '1' if origCommand['showCommandTitle'] is True else '0'

        return f'# DBTITLE {showCommandTitleString},{origCommand["commandTitle"]}\n{commandCode}'
