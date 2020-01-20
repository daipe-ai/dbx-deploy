from pathlib import PurePosixPath
from pygit2 import Repository

class ProjectRootPathFactory:

    def __init__(self, projectRootPathTemplate: str):
        self.__projectRootPathTemplate = projectRootPathTemplate

    def create(self):
        currentGitBranch = Repository('.').head.shorthand

        return PurePosixPath(self.__projectRootPathTemplate.replace('{currentBranch}', currentGitBranch))
