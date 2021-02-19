import re

class PackageInstaller:

    def __init__(
        self,
        packageBaseDir: str,
        offlineInstall: bool,
    ):
        self.__packageBaseDir = packageBaseDir
        self.__offlineInstall = offlineInstall

    def getPackageInstallCommand(self, packageFilePath: str, dependenciesDirPath: str):
        if self.__offlineInstall:
            return self.__getOfflineInstallCommand(packageFilePath, dependenciesDirPath)

        return self.__getOnlineInstallCommand(packageFilePath)

    def isPackageInstallCommand(self, commandCode: str):
        regExp = '^' + re.escape(f'%pip install {self.__modifyDbfs(self.__packageBaseDir)}') + '.+-py3-none-any.whl'

        return re.match(regExp, commandCode) is not None

    def __modifyDbfs(self, path: str):
        return '/dbfs/' + path.lstrip('dbfs:/')

    def __getOnlineInstallCommand(self, packageFilePath: str):
        return f'%pip install {self.__modifyDbfs(packageFilePath)}'

    def __getOfflineInstallCommand(self, packageFilePath: str, dependenciesDirPath: str):
        return f'%pip install {self.__modifyDbfs(packageFilePath)} --no-index --find-links {self.__modifyDbfs(dependenciesDirPath)}'
