import sys
from pathlib import Path
from dbxdeploy.poetry.PoetryPathResolver import PoetryPathResolver
from dbxdeploy.shell.runner import run_and_read_output


class RequirementsCreator:
    def __init__(self, poetry_path_resolver: PoetryPathResolver):
        self.__poetry_path_resolver = poetry_path_resolver

    def export_to_string(self, base_path: Path, only_dependencies=False) -> str:
        python_executable = sys.executable
        poetry_path = self.__poetry_path_resolver.get_poetry_path()
        output = run_and_read_output(
            f"{python_executable} {poetry_path} export -f requirements.txt --without-hashes", cwd=str(base_path), shell=True
        )

        if only_dependencies:
            output = self.__remove_non_dependency_lines(output)

        return output

    def export_to_file(self, base_path: Path, requirements_path: Path, only_dependencies=False) -> None:
        python_executable = sys.executable
        poetry_path = self.__poetry_path_resolver.get_poetry_path()
        output = run_and_read_output(
            f"{python_executable} {poetry_path} export -f requirements.txt --without-hashes", cwd=str(base_path), shell=True
        )

        if only_dependencies:
            output = self.__remove_non_dependency_lines(output)

        with requirements_path.open("w") as file:
            file.write(output)

    def __remove_non_dependency_lines(self, requirements: str) -> str:
        requirements_lines = requirements.split("\n")
        dependency_lines = []

        for line in requirements_lines:
            if not line.strip():
                continue

            if line.startswith("--index-url"):
                continue

            if line.startswith("--extra-index-url"):
                continue

            dependency_lines.append(line)

        return "\n".join(dependency_lines)
