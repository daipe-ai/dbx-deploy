import sys
from pathlib import Path
from dbxdeploy.poetry.PoetryPathResolver import PoetryPathResolver
from dbxdeploy.shell.runner import run_and_read_output


class RequirementsCreator:
    def __init__(self, poetry_path_resolver: PoetryPathResolver):
        self.__poetry_path_resolver = poetry_path_resolver

    def export_to_string(self, base_path: Path, dev_dependencies: bool = False) -> str:
        return self.__generate_dependencies(base_path, dev_dependencies)

    def export_to_file(self, base_path: Path, requirements_path: Path, dev_dependencies=False) -> None:
        dependencies = self.__generate_dependencies(base_path, dev_dependencies)

        with requirements_path.open("w") as file:
            file.write(dependencies)

    def __generate_dependencies(self, base_path: Path, dev_dependencies: bool) -> str:
        python_executable = sys.executable
        poetry_path = self.__poetry_path_resolver.get_poetry_path()
        command = f"{python_executable} {poetry_path} export -f requirements.txt --without-hashes"

        if dev_dependencies:
            command += " --dev"

        output = run_and_read_output(command, cwd=str(base_path), shell=True)

        return output
