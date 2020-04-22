import re
from dbxdeploy.package.PackageInstaller import PackageInstaller

class CommandConverter:

    def __init__(
        self,
        packageInstaller: PackageInstaller,
    ):
        self.__packageInstaller = packageInstaller

    def convert(self, command: dict):
        magicCommand = self.__detectMagicCommand(command['command'])

        if magicCommand in ['%run', '%md', '%sql', '%sh', '%python', '%scala', '%r']:
            commandCode = '# MAGIC ' + command['command'].replace('\n', '\n# MAGIC ')
            return self.__processTitle(commandCode, command)

        if self.__packageInstaller.isPackageInstallCommand(command['command']):
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
