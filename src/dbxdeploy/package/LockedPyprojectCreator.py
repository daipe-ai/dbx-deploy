import tomlkit
from tomlkit import table
from tomlkit.toml_document import TOMLDocument
from pathlib import Path
from dbxdeploy.package.RequirementsLineConverter import RequirementsLineConverter
from dbxdeploy.package.RequirementsGenerator import RequirementsGenerator
from dbxdeploy.package.RequirementsConfig import RequirementsConfig
from dbxdeploy.package.PackageMetadata import PackageMetadata


class LockedPyprojectCreator:
    def __init__(
        self,
        requirements_line_converter: RequirementsLineConverter,
        requirements_generator: RequirementsGenerator,
    ):
        self.__requirements_line_converter = requirements_line_converter
        self.__requirements_generator = requirements_generator

    def create(self, package_metadata: PackageMetadata, pyproject_orig_path: Path, pyproject_new_path: Path):
        toml_doc = self.get_locked_pyproject_toml(package_metadata, pyproject_orig_path)

        with pyproject_new_path.open("w") as t:
            t.write(toml_doc.as_string())

    def get_locked_pyproject_toml(self, package_metadata: PackageMetadata, pyproject_orig_path: Path) -> TOMLDocument:
        main_dependencies = self.__load_main_dependencies()
        toml_doc = self.__generate_pyproject_new(package_metadata, pyproject_orig_path, main_dependencies)

        return toml_doc

    def __load_main_dependencies(self) -> list:
        requirements_config = RequirementsConfig()
        requirements_config.exclude_index_info()
        requirements_txt = self.__requirements_generator.generate(requirements_config)

        return list(map(self.__requirements_line_converter.parse, requirements_txt.splitlines()))

    def __generate_pyproject_new(self, package_metadata: PackageMetadata, pyproject_orig_path: Path, requirements: list) -> TOMLDocument:
        with pyproject_orig_path.open("r") as t:
            toml_doc = tomlkit.parse(t.read())

            dependencies = toml_doc["tool"]["poetry"]["dependencies"]

            if "python" not in dependencies:
                raise Exception('"python" must be defined in [tool.poetry.dependencies]')

            new_dependencies = table()
            new_dependencies.add("python", dependencies["python"])

            for requirement in requirements:
                if self.__is_linux_dependency(requirement):
                    new_dependencies.add(*requirement)

            toml_doc["tool"]["poetry"]["version"] = package_metadata.package_version
            toml_doc["tool"]["poetry"]["dependencies"] = new_dependencies
            del toml_doc["tool"]["poetry"]["dev-dependencies"]

        return toml_doc

    def __is_linux_dependency(self, requirement):
        markers_present = isinstance(requirement[1], dict) and "markers" in requirement[1]

        if not markers_present:
            return True

        platform_info_present = "sys_platform" in requirement[1]["markers"] or "platform_system" in requirement[1]["markers"]

        if not platform_info_present:
            return True

        is_linux_dependency = (
            'sys_platform == "linux"' in requirement[1]["markers"]
            or 'sys_platform == "linux2"' in requirement[1]["markers"]
            or 'platform_system == "Linux"' in requirement[1]["markers"]
        )

        return is_linux_dependency
