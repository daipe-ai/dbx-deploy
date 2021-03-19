from pygit2 import GitError
from pathlib import PurePosixPath
from dbxdeploy.git.CurrentBranchResolver import CurrentBranchResolver
from dbxdeploy.package.PackageMetadata import PackageMetadata


class TargetPathsResolver:
    def __init__(
        self,
        package_deploy_path: str,
        package_release_path: str,
        dependencies_deploy_path: str,
        dependencies_release_path: str,
        workspace_release_path: str,
        workspace_current_path: str,
        current_branch_resolver: CurrentBranchResolver,
    ):
        self.__package_deploy_path = package_deploy_path
        self.__package_release_path = package_release_path
        self.__dependencies_deploy_path = dependencies_deploy_path
        self.__dependencies_release_path = dependencies_release_path
        self.__workspace_release_path = PurePosixPath(workspace_release_path)
        self.__workspace_current_path = PurePosixPath(workspace_current_path)
        self.__current_branch_resolver = current_branch_resolver

    def get_package_upload_path_for_deploy(self, package_metadata: PackageMetadata):
        return self.__replace_package_path(package_metadata, self.__package_deploy_path)

    def get_package_upload_path_for_release(self, package_metadata: PackageMetadata):
        return self.__replace_package_path(package_metadata, self.__package_release_path)

    def get_dependency_upload_path_for_deploy(self, package_metadata: PackageMetadata, dependency_filename):
        return self.__replace_dependency_path(package_metadata, self.__dependencies_deploy_path, dependency_filename)

    def get_dependency_upload_path_for_release(self, package_metadata: PackageMetadata, dependency_filename):
        return self.__replace_dependency_path(package_metadata, self.__dependencies_release_path, dependency_filename)

    def get_dependencies_upload_dir_for_deploy(self, package_metadata: PackageMetadata):
        return self.__replace_path(package_metadata, self.__dependencies_deploy_path.rstrip("{package_filename}"), None)

    def get_dependencies_upload_dir_for_release(self, package_metadata: PackageMetadata):
        return self.__replace_path(package_metadata, self.__dependencies_release_path.rstrip("{package_filename}"), None)

    def get_workspace_release_path(self, package_metadata: PackageMetadata) -> PurePosixPath:
        return self.__replace_workspace_path(package_metadata, self.__workspace_release_path)

    def get_workspace_current_path(self, package_metadata: PackageMetadata) -> PurePosixPath:
        return self.__replace_workspace_path(package_metadata, self.__workspace_current_path)

    def __replace_package_path(self, package_metadata: PackageMetadata, package_path: str):
        return self.__replace_path(package_metadata, package_path, package_metadata.get_package_filename())

    def __replace_dependency_path(self, package_metadata: PackageMetadata, package_path: str, dependency_filename):
        return self.__replace_path(package_metadata, package_path, dependency_filename)

    def __replace_path(self, package_metadata: PackageMetadata, package_path: str, package_filename: str):
        replacements = {
            "package_name": package_metadata.package_name,
            "package_filename": package_filename,
            "current_time": package_metadata.date_time.strftime("%Y-%m-%d_%H-%M-%S"),
            "random_string": package_metadata.random_string,
        }

        if "{current_branch}" in package_path:
            try:
                replacements["current_branch"] = self.__current_branch_resolver.resolve()
            except GitError:
                replacements["current_branch"] = "__no_git_repo__"

        return package_path.format(**replacements)

    def __replace_workspace_path(self, package_metadata: PackageMetadata, workspace_path: PurePosixPath):
        replacements = {
            "current_time": package_metadata.date_time.strftime("%Y-%m-%d_%H:%M:%S"),
            "random_string": package_metadata.random_string,
        }

        if "{current_branch}" in str(workspace_path):
            replacements["current_branch"] = self.__current_branch_resolver.resolve()

        return PurePosixPath(str(workspace_path).format(**replacements))
