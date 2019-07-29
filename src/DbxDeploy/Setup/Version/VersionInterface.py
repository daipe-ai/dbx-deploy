from abc import ABC

class VersionInterface(ABC):
    pass

    def getWhlVersion(self) -> str:
        pass

    def getDbxVersionPath(self, dbxProjectRoot: str) -> str:
        pass

    def getDbxVersionPathRegEx(self, dbxProjectRoot: str) -> str:
        pass

    def getTimeAndRandomString(self) -> str:
        pass
