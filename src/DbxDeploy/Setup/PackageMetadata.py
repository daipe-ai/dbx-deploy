from DbxDeploy.Setup.Version.VersionInterface import VersionInterface

class PackageMetadata:

    def __init__(
        self,
        packageName: str,
        version: VersionInterface
    ):
        self.__packageName = packageName
        self.__version = version

    def getPackageName(self):
        return self.__packageName

    def getVersion(self):
        return self.__version

    def getWhlPackageName(self):
        return self.__packageName.replace('-', '_')

    def getWhlFileName(self):
        return '{}-{}-py3-none-any.whl'.format(self.getWhlPackageName(), self.__version.getWhlVersion())

    def getCurrentWhlFileName(self):
        return '{}-{}-py3-none-any.whl'.format(self.getWhlPackageName(), 'current')
