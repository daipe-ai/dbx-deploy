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

    def getPackageFilename(self):
        return '{}-{}-py3-none-any.whl'.format(self.__getPackageName(), self.__packageVersion)

    def getPackageUploadPathForRelease(self, dbfsBasePath: PurePosixPath) -> PurePosixPath:
        versionDirName = self.__packageName + '/' + self.__dateTime.strftime('%Y-%m-%d_%H-%M-%S') + '_' + self.__randomString

        return dbfsBasePath.joinpath(versionDirName).joinpath(self.getPackageFilename())

    def getPackageUploadPathForCurrent(self, dbfsBasePath: PurePosixPath) -> PurePosixPath:
        return dbfsBasePath.joinpath(self.__packageName + '/_current').joinpath(self.getPackageFilename())

    def getWorkspaceReleasePath(self, workspaceBaseDir: PurePosixPath) -> PurePosixPath:
        releaseDirName = self.__dateTime.strftime('%Y-%m-%d_%H:%M:%S') + '_' + self.__randomString

        return workspaceBaseDir.joinpath(releaseDirName)

    def getNotebookReleasePath(self, workspaceBaseDir: PurePosixPath, notebookPath: PurePosixPath) -> PurePosixPath:
        return self.getWorkspaceReleasePath(workspaceBaseDir).joinpath(notebookPath)

    def getNotebookPathRegEx(self, workspaceBaseDir: PurePosixPath, notebookPath: PurePosixPath) -> str:
        return '^' + str(workspaceBaseDir) + '/([^/]+)/' + str(notebookPath) + '$'

    def getJobRunName(self) -> str:
        return self.__dateTime.strftime('%Y-%m-%d_%H:%M:%S') + '_' + self.__randomString

    def __getPackageName(self):
        return self.__packageName.replace('-', '_')
