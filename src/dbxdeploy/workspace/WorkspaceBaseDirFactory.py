from pathlib import PurePosixPath
from pygit2 import Repository, GitError # pylint: disable = no-name-in-module

class WorkspaceBaseDirFactory:

    def __init__(self, workspaceBaseDirTemplate: str):
        self.__workspaceBaseDirTemplate = workspaceBaseDirTemplate

    def create(self):
        try:
            currentGitBranch = Repository('.').head.shorthand
        except GitError as e:
            if str(e) != 'Repository not found at .':
                raise

            currentGitBranch = 'git_repo_missing'

        return PurePosixPath(self.__workspaceBaseDirTemplate.replace('{currentBranch}', currentGitBranch))
