import tomlkit
from tomlkit.items import Table
from typing import List
from pathlib import Path
from dbxdeploy.package.Dependency import Dependency
from dbxdeploy.package.RequirementsLineConverter import RequirementsLineConverter
from dbxdeploy.package.RequirementsGenerator import RequirementsGenerator
from dbxdeploy.package.RequirementsConfig import RequirementsConfig


class PackageDependencyLoader:
    def __init__(
        self,
        requirements_line_converter: RequirementsLineConverter,
        requirements_generator: RequirementsGenerator,
    ):
        self.__requirements_generator = requirements_generator
        self.__requirements_line_converter = requirements_line_converter

    def load(self, project_base_dir: Path) -> List[Dependency]:
        poetry_lock_path = project_base_dir.joinpath("poetry.lock")
        poetry_lock_dependencies = self.__load_poetry_lock_dependencies(poetry_lock_path)

        main_dependencies = self.__load_main_dependencies()
        dependencies = []

        for dependency in main_dependencies:
            dependency_name = dependency[0]
            dependencies.append(
                Dependency(dependency_name, self.__find_poetry_lock_version_by_name(poetry_lock_dependencies, dependency_name))
            )

        return dependencies

    def __load_main_dependencies(self) -> list:
        requirements_config = RequirementsConfig()
        requirements_config.exclude_index_info()
        requirements_txt = self.__requirements_generator.generate(requirements_config)

        return list(map(self.__requirements_line_converter.parse, requirements_txt.splitlines()))

    def __load_poetry_lock_dependencies(self, lockfile_path: Path) -> List[Table]:
        with lockfile_path.open("r") as f:
            config = tomlkit.parse(f.read())

        return [package for package in config["package"] if package["category"] == "main" and package["name"]]

    def __find_poetry_lock_version_by_name(self, dependencies: List[Table], dependency_name: str) -> str:
        for dependency in dependencies:
            if dependency["name"].lower() == dependency_name.lower():
                return dependency["version"]

        raise Exception(f"Dependency {dependency_name} not found in poetry.lock")
