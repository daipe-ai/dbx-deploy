from typing import Iterable
from pathlib import Path
from dbxdeploy.package.PackageMetadata import PackageMetadata
from dbxdeploy.package.Dependency import Dependency

class LocalPathsResolver:

    def __init__(
        self,
        projectBaseDir: Path,
    ):
        self.__projectBaseDir = projectBaseDir

    def getPackageDistPath(self, packageMetadata: PackageMetadata):
        distDir = self.__projectBaseDir.joinpath('dist')

        return distDir.joinpath(packageMetadata.getPackageFilename())

    def getDependencyDistPath(self, dependency: Dependency):
        distDir = self.__projectBaseDir.joinpath('dist')

        return self.getDependencyPathFromDir(distDir, dependency)

    def getDependencyPathFromDir(self, directory: Path, dependency: Dependency):
        dependencyPaths = self.__getAllDependencyPathsFromDir(directory)
        dependencyPath = self.__findDependencyPath(dependencyPaths, dependency)

        if dependencyPath:
            return dependencyPath

        raise Exception(f'Dependency {dependency.dependencyName}=={dependency.dependencyVersion} not found in {directory} directory')

    def getLinuxDependencyPathFromDir(self, directory: Path, dependency: Dependency):
        dependencyPaths = self.__getLinuxDependencyPathsFromDir(directory)
        dependencyPath = self.__findDependencyPath(dependencyPaths, dependency)

        if dependencyPath:
            return dependencyPath

        raise Exception(f'Linux Dependency {dependency.dependencyName}=={dependency.dependencyVersion} not found in {directory} directory')

    def getDependencyFilenameFromPath(self, dependencyPath: Path):
        return dependencyPath.name

    def __getDependencyNameFromPath(self, dependencyPath: Path):
        return dependencyPath.stem.split('-')[0].replace('_', '-')

    def __getDependencyVersionFromPath(self, dependencyPath: Path):
        return dependencyPath.stem.split('-')[1]

    def __getDependencyPlatformFromPath(self, dependencyPath: Path):
        return dependencyPath.stem.split('-')[-1]

    def __getAllDependencyPathsFromDir(self, directory: Path):
        return directory.glob('*.whl')

    def __getLinuxDependencyPathsFromDir(self, directory: Path):
        return [dependencyPath for dependencyPath in directory.glob('*.whl') if self.__isLinuxDependency(dependencyPath)]

    def __isLinuxDependency(self, dependencyPath: Path):
        platform = self.__getDependencyPlatformFromPath(dependencyPath).lower()

        return platform == 'any' or 'linux' in platform

    def __findDependencyPath(self, dependencyPaths: Iterable[Path], dependency: Dependency):
        for dependencyPath in dependencyPaths:
            wheelName = self.__getDependencyNameFromPath(dependencyPath)
            wheelVersion = self.__getDependencyVersionFromPath(dependencyPath)

            if wheelName.lower() == dependency.dependencyName.lower() and wheelVersion == dependency.dependencyVersion:
                return dependencyPath

        return None
