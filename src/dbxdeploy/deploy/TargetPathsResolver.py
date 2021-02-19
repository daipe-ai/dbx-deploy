from pygit2 import GitError # pylint: disable = no-name-in-module
from pathlib import PurePosixPath
from dbxdeploy.git.CurrentBranchResolver import CurrentBranchResolver
from dbxdeploy.package.PackageMetadata import PackageMetadata

class TargetPathsResolver:

    def __init__(
        self,
        packageDeployPath: str,
        packageReleasePath: str,
        dependenciesDeployPath: str,
        dependenciesReleasePath: str,
        workspaceReleasePath: str,
        workspaceCurrentPath: str,
        currentBranchResolver: CurrentBranchResolver,
    ):
        self.__packageDeployPath = packageDeployPath
        self.__packageReleasePath = packageReleasePath
        self.__dependenciesDeployPath = dependenciesDeployPath
        self.__dependenciesReleasePath = dependenciesReleasePath
        self.__workspaceReleasePath = PurePosixPath(workspaceReleasePath)
        self.__workspaceCurrentPath = PurePosixPath(workspaceCurrentPath)
        self.__currentBranchResolver = currentBranchResolver

    def getPackageUploadPathForDeploy(self, packageMetadata: PackageMetadata):
        return self.__replacePackagePath(packageMetadata, self.__packageDeployPath)

    def getPackageUploadPathForRelease(self, packageMetadata: PackageMetadata):
        return self.__replacePackagePath(packageMetadata, self.__packageReleasePath)

    def getDependencyUploadPathForDeploy(self, packageMetadata: PackageMetadata, dependencyFilename):
        return self.__replaceDependencyPath(packageMetadata, self.__dependenciesDeployPath, dependencyFilename)

    def getDependencyUploadPathForRelease(self, packageMetadata: PackageMetadata, dependencyFilename):
        return self.__replaceDependencyPath(packageMetadata, self.__dependenciesReleasePath, dependencyFilename)

    def getDependenciesUploadDirForDeploy(self, packageMetadata: PackageMetadata):
        return self.__replacePath(packageMetadata, self.__dependenciesDeployPath.rstrip('{packageFilename}'), None)

    def getDependenciesUploadDirForRelease(self, packageMetadata: PackageMetadata):
        return self.__replacePath(packageMetadata, self.__dependenciesReleasePath.rstrip('{packageFilename}'), None)

    def getWorkspaceReleasePath(self, packageMetadata: PackageMetadata) -> PurePosixPath:
        return self.__replaceWorkspacePath(packageMetadata, self.__workspaceReleasePath)

    def getWorkspaceCurrentPath(self, packageMetadata: PackageMetadata) -> PurePosixPath:
        return self.__replaceWorkspacePath(packageMetadata, self.__workspaceCurrentPath)

    def __replacePackagePath(self, packageMetadata: PackageMetadata, packagePath: str):
        return self.__replacePath(packageMetadata, packagePath, packageMetadata.getPackageFilename())

    def __replaceDependencyPath(self, packageMetadata: PackageMetadata, packagePath: str, dependencyFilename):
        return self.__replacePath(packageMetadata, packagePath, dependencyFilename)

    def __replacePath(self, packageMetadata: PackageMetadata, packagePath: str, packageFilename: str):
        replacements = {
            'packageName': packageMetadata.packageName,
            'packageFilename': packageFilename,
            'currentTime': packageMetadata.dateTime.strftime('%Y-%m-%d_%H-%M-%S'),
            'randomString': packageMetadata.randomString,
        }

        if '{currentBranch}' in packagePath:
            try:
                replacements['currentBranch'] = self.__currentBranchResolver.resolve()
            except GitError:
                replacements['currentBranch'] = '__no_git_repo__'

        return packagePath.format(**replacements)

    def __replaceWorkspacePath(self, packageMetadata: PackageMetadata, workspacePath: PurePosixPath):
        replacements = {
            'currentTime': packageMetadata.dateTime.strftime('%Y-%m-%d_%H:%M:%S'),
            'randomString': packageMetadata.randomString,
        }

        if '{currentBranch}' in str(workspacePath):
            replacements['currentBranch'] = self.__currentBranchResolver.resolve()

        return PurePosixPath(str(workspacePath).format(**replacements))
