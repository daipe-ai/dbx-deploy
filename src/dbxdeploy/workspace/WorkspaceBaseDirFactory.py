from pathlib import PurePosixPath
from dbxdeploy.git.CurrentBranchResolver import CurrentBranchResolver


class WorkspaceBaseDirFactory:

    current_branch_placeholder = "{current_branch}"

    def __init__(
        self,
        workspace_base_dir_template: str,
        current_branch_resolver: CurrentBranchResolver,
    ):
        self.__workspace_base_dir_template = workspace_base_dir_template
        self.__current_branch_resolver = current_branch_resolver

    def create(self):
        if self.current_branch_placeholder not in self.__workspace_base_dir_template:
            return PurePosixPath(self.__workspace_base_dir_template)

        current_git_branch = self.__current_branch_resolver.resolve()

        return PurePosixPath(self.__workspace_base_dir_template.replace(self.current_branch_placeholder, current_git_branch))
