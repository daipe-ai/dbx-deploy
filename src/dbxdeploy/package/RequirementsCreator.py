import sys
from pathlib import Path
from dbxdeploy.poetry.PoetryPathResolver import PoetryPathResolver
from dbxdeploy.shell.runner import runAndReadOutput
from dbxdeploy.shell.runner import runShellCommand

class RequirementsCreator:

    def __init__(
        self,
        poetryPathResolver: PoetryPathResolver
    ):
        self.__poetryPathResolver = poetryPathResolver

    def exportToString(self, basePath: Path) -> str:
        pythonExecutable = sys.executable
        poetryPath = self.__poetryPathResolver.getPoetryPath()
        output = runAndReadOutput(f'{pythonExecutable} {poetryPath} export -f requirements.txt --without-hashes', cwd=str(basePath), shell=True)

        return output

    def exportToFile(self, basePath: Path, requirementsPath: Path) -> None:
        pythonExecutable = sys.executable
        poetryPath = self.__poetryPathResolver.getPoetryPath()
        runShellCommand(f'{pythonExecutable} {poetryPath} export -f requirements.txt -o {requirementsPath} --without-hashes', cwd=str(basePath), shell=True)
