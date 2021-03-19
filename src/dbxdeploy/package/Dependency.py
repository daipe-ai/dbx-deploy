class Dependency:
    def __init__(
        self,
        dependency_name: str,
        dependency_version: str,
    ):

        self.__dependency_name = dependency_name
        self.__dependency_version = dependency_version

    @property
    def dependency_name(self):
        return self.__dependency_name

    @property
    def dependency_version(self):
        return self.__dependency_version
