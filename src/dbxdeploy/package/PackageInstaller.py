import re

class PackageInstaller:

    def __init__(
        self,
        packageBaseDir: str,
    ):
        self.__packageBaseDir = packageBaseDir

    def getPackageInstallCommand(self, packageFilePath: str):
        return 'dbutils.library.install(\'{}\')'.format(packageFilePath)

    def isPackageInstallCommand(self, commandCode: str):
        regExp = '^' + re.escape('dbutils.library.install(\'' + self.__packageBaseDir) + '.+-py3-none-any.whl\'\\)$'

        return re.match(regExp, commandCode) is not None
