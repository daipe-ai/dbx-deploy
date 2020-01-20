from datetime import datetime
from pathlib import PurePosixPath

class PackageMetadata:

    def __init__(
        self,
        packageName: str,
        packageVersion: float,
        dateTime: datetime,
        randomString: str
    ):
        self.__packageName = packageName
        self.__packageVersion = packageVersion
        self.__dateTime = dateTime
        self.__randomString = randomString

    def getWhlFileName(self):
        return '{}-{}-py3-none-any.whl'.format(self.__getWhlPackageName(), self.__packageVersion)

    def getWhlUploadPathForRelease(self, dbfsBasePath: PurePosixPath) -> PurePosixPath:
        versionDirName = self.__packageName + '/' + self.__dateTime.strftime('%Y-%m-%d_%H-%M-%S') + '_' + self.__randomString

        return dbfsBasePath.joinpath(versionDirName).joinpath(self.getWhlFileName())

    def getWhlUploadPathForCurrent(self, dbfsBasePath: PurePosixPath) -> PurePosixPath:
        return dbfsBasePath.joinpath(self.__packageName + '/_current').joinpath(self.getWhlFileName())

    def getWorkspaceReleasePath(self, dbxProjectRoot: PurePosixPath) -> PurePosixPath:
        releaseDirName = self.__dateTime.strftime('%Y-%m-%d_%H:%M:%S') + '_' + self.__randomString

        return dbxProjectRoot.joinpath(releaseDirName)

    def getNotebookReleasePath(self, dbxProjectRoot: PurePosixPath, notebookPath: PurePosixPath) -> PurePosixPath:
        return self.getWorkspaceReleasePath(dbxProjectRoot).joinpath(notebookPath)

    def getNotebookPathRegEx(self, dbxProjectRoot: PurePosixPath, notebookPath: PurePosixPath) -> str:
        return '^' + str(dbxProjectRoot) + '/([^/]+)/' + str(notebookPath) + '$'

    def getJobRunName(self) -> str:
        return self.__dateTime.strftime('%Y-%m-%d_%H:%M:%S') + '_' + self.__randomString

    def __getWhlPackageName(self):
        return self.__packageName.replace('-', '_')
