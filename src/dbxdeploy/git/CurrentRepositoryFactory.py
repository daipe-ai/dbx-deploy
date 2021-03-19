from pathlib import Path
from pygit2 import Repository, discover_repository, GitError


class CurrentRepositoryFactory:
    def __init__(
        self,
        base_path: Path,
    ):
        self.__base_path = base_path

    def create(self):
        repository_path = discover_repository(self.__base_path.as_posix())

        if not repository_path:
            raise GitError(f'No repository found at "{self.__base_path}" and its parents')

        return Repository(repository_path)
