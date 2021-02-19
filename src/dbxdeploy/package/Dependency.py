class Dependency:

    def __init__(
        self,
        dependencyName: str,
        dependencyVersion: str,
    ):

        self.__dependencyName = dependencyName
        self.__dependencyVersion = dependencyVersion

    @property
    def dependencyName(self):
        return self.__dependencyName

    @property
    def dependencyVersion(self):
        return self.__dependencyVersion
