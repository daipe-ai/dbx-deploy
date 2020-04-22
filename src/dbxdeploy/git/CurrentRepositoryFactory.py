from pathlib import Path
from pygit2 import Repository, discover_repository, GitError # pylint: disable = no-name-in-module

class CurrentRepositoryFactory:

    def __init__(
        self,
        basePath: Path,
    ):
        self.__basePath = basePath

    def create(self):
        repositoryPath = discover_repository(self.__basePath.as_posix())

        if not repositoryPath:
            raise GitError(f'No repository found at "{self.__basePath}" and its parents')

        return Repository(repositoryPath)
