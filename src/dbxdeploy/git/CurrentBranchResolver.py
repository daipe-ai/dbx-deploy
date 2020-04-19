from pygit2 import Repository # pylint: disable = no-name-in-module

class CurrentBranchResolver:

    def __init__(
        self,
        repositoryBaseDir: str,
    ):
        self.__repositoryBaseDir = repositoryBaseDir

    def resolve(self) -> str:
        return Repository(self.__repositoryBaseDir).head.shorthand
