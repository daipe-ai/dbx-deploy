import tomlkit
from tomlkit import table
from tomlkit.toml_document import TOMLDocument
from pathlib import Path
from dbxdeploy.package.RequirementsLineConverter import RequirementsLineConverter
from dbxdeploy.package.RequirementsCreator import RequirementsCreator


class LockedPyprojectCreator:
    def __init__(
        self,
        requirements_line_converter: RequirementsLineConverter,
        requirements_creator: RequirementsCreator,
    ):
        self.__requirements_line_converter = requirements_line_converter
        self.__requirements_creator = requirements_creator

    def create(self, base_path: Path, pyproject_orig_path: Path, pyproject_new_path: Path):
        toml_doc = self.get_locked_pyproject_toml(base_path, pyproject_orig_path)

        with pyproject_new_path.open("w") as t:
            t.write(toml_doc.as_string())

    def get_locked_pyproject_toml(self, base_path: Path, pyproject_orig_path: Path) -> TOMLDocument:
        main_dependencies = self.__load_main_dependencies(base_path)
        toml_doc = self.__generate_pyproject_new(pyproject_orig_path, main_dependencies)

        return toml_doc

    def __load_main_dependencies(self, base_path: Path) -> list:
        requirements = self.__requirements_creator.export_to_string(base_path).splitlines()
        requirements = [
            requirement
            for requirement in requirements
            if not requirement.strip() == ""
            and not requirement.startswith("--index-url")
            and not requirement.startswith("--extra-index-url")
        ]

        return list(map(self.__requirements_line_converter.parse, requirements))

    def __generate_pyproject_new(self, pyproject_orig_path: Path, requirements: list) -> TOMLDocument:
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
