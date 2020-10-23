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

    @property
    def packageName(self):
        return self.__packageName

    @property
    def packageVersion(self):
        return self.__packageVersion

    @property
    def dateTime(self):
        return self.__dateTime

    @property
    def randomString(self):
        return self.__randomString

    def getPackageFilename(self):
        return '{}-{}-py3-none-any.whl'.format(self.__getPackageName(), self.__packageVersion)

    def getNotebookPathRegEx(self, workspaceBaseDir: PurePosixPath, notebookPath: PurePosixPath) -> str:
        return '^' + str(workspaceBaseDir) + '/([^/]+)/' + str(notebookPath) + '$'

    def getJobRunName(self) -> str:
        return self.__dateTime.strftime('%Y-%m-%d_%H:%M:%S') + '_' + self.__randomString

    def __getPackageName(self):
        return self.__packageName.replace('-', '_')
