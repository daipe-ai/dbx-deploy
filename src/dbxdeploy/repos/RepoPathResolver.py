class RepoPathResolver:
    def __init__(
        self,
        repo_root_dir: str,
        repo_path: str,
        repo_base_dir: str,
    ):
        if repo_root_dir is not None or repo_path is not None:
            raise Exception(
                "dbxdeploy.target.repo.root_dir and dbxdeploy.target.repo.path are deprecated, please use dbxdeploy.target.repo.base_dir instead"
            )

        self.__repo_base_dir = repo_base_dir

    def resolve(self, repo_name: str = None, branch: str = None, tag: str = None):
        self.__validate_placeholder_arguments("{repo_name}", repo_name, "--repo_name")
        self.__validate_placeholder_arguments("{branch_name}", branch, "--branch")
        self.__validate_placeholder_arguments("{tag_name}", tag, "--tag")
        return self.__repo_base_dir.format(repo_name=repo_name, branch_name=branch, tag_name=tag)

    def __validate_placeholder_arguments(self, placeholder, argument, argument_name):
        if argument is None and placeholder in self.__repo_base_dir:
            raise Exception(f"{placeholder} used in repo.base_dir, but {argument_name} argument was not provided")
