import tomlkit
from tomlkit.items import Table
from typing import List
from pathlib import Path
from dbxdeploy.package.Dependency import Dependency
from dbxdeploy.package.LockedPyprojectCreator import LockedPyprojectCreator

class PackageDependencyLoader:

    def __init__(
        self,
        lockedPyprojectCreator: LockedPyprojectCreator
    ):
        self.__lockedPyprojectCreator = lockedPyprojectCreator

    def load(self, projectBaseDir: Path) -> List[Dependency]:
        pyprojectPath = projectBaseDir.joinpath('pyproject.toml')
        poetryLockPath = projectBaseDir.joinpath('poetry.lock')
        lockedPyprojectToml = self.__lockedPyprojectCreator.getLockedPyprojectToml(projectBaseDir, pyprojectPath)
        lockedPyprojectDependencies = lockedPyprojectToml['tool']['poetry']['dependencies']
        poetryLockDependencies = self.__loadPoetryLockDependencies(poetryLockPath)
        dependencies = []

        for dependencyName in lockedPyprojectDependencies:
            if dependencyName == 'python':
                continue

            dependencies.append(
                Dependency(
                    dependencyName,
                    self.__findPoetryLockVersionByName(poetryLockDependencies, dependencyName)
                )
            )

        return dependencies

    def __loadPoetryLockDependencies(self, lockfilePath: Path) -> List[Table]:
        with lockfilePath.open('r') as f:
            config = tomlkit.parse(f.read())

        return [package for package in config['package'] if package['category'] == 'main' and package['name']]

    def __findPoetryLockVersionByName(self, dependencies: List[Table], dependencyName: str) -> str:
        for dependency in dependencies:
            if dependency['name'].lower() == dependencyName.lower():
                return dependency['version']

        raise Exception(f'Dependency {dependencyName} not found in poetry.lock')
