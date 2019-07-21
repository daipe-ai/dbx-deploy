from datetime import datetime
from DbxDeploy.Setup.Version.VersionInterface import VersionInterface

class CurrentTimeVersion(VersionInterface):

    def __init__(self, dateTime: datetime, randomString: str):
        self.__dateTime = dateTime
        self.__randomString = randomString

    def getWhlVersion(self) -> str:
        return self.__dateTime.strftime('%d_%m_%H_%M_%S') + '_' + self.__randomString

    def getDbxVersionPath(self, dbxProjectRoot: str) -> str:
        return dbxProjectRoot + '/' + self.__dateTime.strftime('%d.%m_%H:%M:%S') + '_' + self.__randomString
