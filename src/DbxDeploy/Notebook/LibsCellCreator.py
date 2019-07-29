from DbxDeploy.Setup.PackageMetadata import PackageMetadata

class LibsCellCreator:

    def __init__(self, dbfsBasePath):
        self.__dbfsBasePath = dbfsBasePath

    def create(self, packagesToInstall: list, packageMetadata: PackageMetadata):
        lines = []

        whlFilename = self.__dbfsBasePath + '/' + packageMetadata.getWhlFileName()

        lines.append('dbutils.library.install(\'{}\')'.format(whlFilename))

        for name, version in packagesToInstall:
            line = 'dbutils.library.installPyPI(\'{}\', \'{}\')'.format(name, version)
            lines.append(line)

        lines.append('dbutils.library.restartPython()')

        return '\n'.join(lines)
