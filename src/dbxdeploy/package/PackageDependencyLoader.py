import tomlkit
from tomlkit.items import Table
from typing import List
from pathlib import Path
from dbxdeploy.package.Dependency import Dependency
from dbxdeploy.package.LockedPyprojectCreator import LockedPyprojectCreator


class PackageDependencyLoader:
    def __init__(self, locked_pyproject_creator: LockedPyprojectCreator):
        self.__locked_pyproject_creator = locked_pyproject_creator

    def load(self, project_base_dir: Path) -> List[Dependency]:
        pyproject_path = project_base_dir.joinpath("pyproject.toml")
        poetry_lock_path = project_base_dir.joinpath("poetry.lock")
        locked_pyproject_toml = self.__locked_pyproject_creator.get_locked_pyproject_toml(project_base_dir, pyproject_path)
        locked_pyproject_dependencies = locked_pyproject_toml["tool"]["poetry"]["dependencies"]
        poetry_lock_dependencies = self.__load_poetry_lock_dependencies(poetry_lock_path)
        dependencies = []

        for dependency_name in locked_pyproject_dependencies:
            if dependency_name == "python":
                continue

            dependencies.append(
                Dependency(dependency_name, self.__find_poetry_lock_version_by_name(poetry_lock_dependencies, dependency_name))
            )

        return dependencies

    def __load_poetry_lock_dependencies(self, lockfile_path: Path) -> List[Table]:
        with lockfile_path.open("r") as f:
            config = tomlkit.parse(f.read())

        return [package for package in config["package"] if package["category"] == "main" and package["name"]]

    def __find_poetry_lock_version_by_name(self, dependencies: List[Table], dependency_name: str) -> str:
        for dependency in dependencies:
            if dependency["name"].lower() == dependency_name.lower():
                return dependency["version"]

        raise Exception(f"Dependency {dependency_name} not found in poetry.lock")
