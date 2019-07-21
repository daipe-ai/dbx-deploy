from DbxDeploy.Setup.Version.VersionInterface import VersionInterface

class LibsCellCreator:

    def __init__(self, dbfsBasePath):
        self.__dbfsBasePath = dbfsBasePath

    def create(self, packagesToInstall: list, version: VersionInterface):
        lines = []

        whlFilename = self.__dbfsBasePath + '/dev_env-{}-py3-none-any.whl'.format(version.getWhlVersion())

        lines.append('dbutils.library.install(\'{}\')'.format(whlFilename))

        for name, version in packagesToInstall:
            line = 'dbutils.library.installPyPI(\'{}\', \'{}\')'.format(name, version)
            lines.append(line)

        lines.append('dbutils.library.restartPython()')

        return '\n'.join(lines)
