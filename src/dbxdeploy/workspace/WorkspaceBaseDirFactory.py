from pathlib import PurePosixPath
from dbxdeploy.git.CurrentBranchResolver import CurrentBranchResolver

class WorkspaceBaseDirFactory:

    currentBranchPlaceholder = '{currentBranch}'

    def __init__(
        self,
        workspaceBaseDirTemplate: str,
        currentBranchResolver: CurrentBranchResolver,
    ):
        self.__workspaceBaseDirTemplate = workspaceBaseDirTemplate
        self.__currentBranchResolver = currentBranchResolver

    def create(self):
        if self.currentBranchPlaceholder not in self.__workspaceBaseDirTemplate:
            return PurePosixPath(self.__workspaceBaseDirTemplate)

        currentGitBranch = self.__currentBranchResolver.resolve()

        return PurePosixPath(self.__workspaceBaseDirTemplate.replace(self.currentBranchPlaceholder, currentGitBranch))
