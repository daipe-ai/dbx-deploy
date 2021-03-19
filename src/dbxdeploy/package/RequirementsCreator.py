import sys
from pathlib import Path
from dbxdeploy.poetry.PoetryPathResolver import PoetryPathResolver
from dbxdeploy.shell.runner import run_and_read_output
from dbxdeploy.shell.runner import run_shell_command


class RequirementsCreator:
    def __init__(self, poetry_path_resolver: PoetryPathResolver):
        self.__poetry_path_resolver = poetry_path_resolver

    def export_to_string(self, base_path: Path) -> str:
        python_executable = sys.executable
        poetry_path = self.__poetry_path_resolver.get_poetry_path()
        output = run_and_read_output(
            f"{python_executable} {poetry_path} export -f requirements.txt --without-hashes", cwd=str(base_path), shell=True
        )

        return output

    def export_to_file(self, base_path: Path, requirements_path: Path) -> None:
        python_executable = sys.executable
        poetry_path = self.__poetry_path_resolver.get_poetry_path()
        run_shell_command(
            f"{python_executable} {poetry_path} export -f requirements.txt -o {requirements_path} --without-hashes",
            cwd=str(base_path),
            shell=True,
        )
