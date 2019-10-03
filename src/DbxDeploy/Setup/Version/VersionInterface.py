from abc import ABC
from pathlib import PurePosixPath

class VersionInterface(ABC):

    def getWhlVersion(self) -> str:
        pass

    def getDbxVersionPath(self, dbxProjectRoot: PurePosixPath) -> PurePosixPath:
        pass

    def getDbxVersionPathRegEx(self, dbxProjectRoot: PurePosixPath) -> str:
        pass

    def getTimeAndRandomString(self) -> str:
        pass
