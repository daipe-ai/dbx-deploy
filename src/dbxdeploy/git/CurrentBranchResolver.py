from pathlib import Path
from pygit2 import Repository, discover_repository, GitError  # pyre-ignore  # pylint: disable = no-name-in-module


class CurrentBranchResolver:
    def __init__(
        self,
        base_path: Path,
    ):
        self.__base_path = base_path

    def resolve(self):
        repository_path = discover_repository(self.__base_path.as_posix())

        if not repository_path:
            raise GitError(f'No repository found at "{self.__base_path}" and its parents')

        return Repository(repository_path).head.shorthand
