import sys
import re
from typing import List
from pathlib import Path
from dbxdeploy.poetry.PoetryPathResolver import PoetryPathResolver
from dbxdeploy.package.RequirementsConfig import RequirementsConfig
from dbxdeploy.shell.runner import run_and_read_output
from dbxdeploy.package.requirements_regex import LOCAL_FILE_LINE_REGEX


class RequirementsGenerator:
    def __init__(
        self,
        project_base_dir: Path,
        poetry_path_resolver: PoetryPathResolver,
    ):
        self.__project_base_dir = project_base_dir
        self.__poetry_path_resolver = poetry_path_resolver
        self.__python_executable = sys.executable

    def generate(self, requirements_config: RequirementsConfig) -> str:
        options = ["--format requirements.txt", "--without-hashes"]

        if requirements_config.should_include_dev_dependencies:
            options.append("--dev")

        if requirements_config.should_include_credentials:
            options.append("--with-credentials")

        requirements_txt = self.__generate_requirements_txt(options)

        if requirements_config.should_exclude_index_info:
            requirements_txt = self.__remove_index_info(requirements_txt)

        if requirements_config.should_exclude_file_dependencies:
            requirements_txt = self.__remove_file_dependencies(requirements_txt)

        if requirements_config.should_redact_credentials:
            requirements_txt = self.__redact_credentials(requirements_txt)

        return requirements_txt

    def __generate_requirements_txt(self, options: List[str]) -> str:
        command = f"{self.__python_executable} {self.__poetry_path_resolver.get_poetry_path()} export {' '.join(options)}"

        output = run_and_read_output(command, cwd=str(self.__project_base_dir), shell=True)

        return output

    def __remove_index_info(self, requirements_txt: str) -> str:
        requirements = requirements_txt.splitlines()

        requirements = [
            requirement
            for requirement in requirements
            if not requirement.strip() == ""
            and not requirement.startswith("--index-url")
            and not requirement.startswith("--extra-index-url")
        ]

        return "\n".join(requirements)

    def __remove_file_dependencies(self, requirements_txt: str) -> str:
        requirements = requirements_txt.splitlines()

        requirements = [requirement for requirement in requirements if not re.match(LOCAL_FILE_LINE_REGEX, requirement)]

        return "\n".join(requirements)

    def __redact_credentials(self, requirements_txt: str) -> str:
        requirements = requirements_txt.splitlines()

        for index, line in enumerate(requirements):
            if line.startswith("--index-url") and "@" in line or line.startswith("--extra-index-url") and "@" in line:
                matches = re.match(r"(.*http://|.*https://)(.*?)(@.*)", line)
                redacted_line = matches.group(1) + "[REDACTED]" + matches.group(3)
                requirements[index] = redacted_line

        return "\n".join(requirements)
