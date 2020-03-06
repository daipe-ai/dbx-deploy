import subprocess
import tomlkit
from tomlkit import table
from tomlkit.toml_document import TOMLDocument
from pathlib import Path
from dbxdeploy.whl.RequirementsLineConverter import RequirementsLineConverter

class WhlBuilder:

    def __init__(
        self,
        requirementsLineConverter: RequirementsLineConverter,
    ):
        self.__requirementsLineConverter = requirementsLineConverter

    def build(self, basePath: Path):
        basePath.joinpath('dist').mkdir(exist_ok=True)
        requirementsPath = basePath.joinpath('dist/requirements.txt')

        pyprojectOrigPath = basePath.joinpath('pyproject.toml')
        pyprojectNewPath = basePath.joinpath('pyproject.toml.new')

        subprocess.run(f'poetry export -f requirements.txt -o {requirementsPath} --without-hashes', check=True, cwd=str(basePath), shell=True)

        requirements = self.__readRequirements(requirementsPath)
        tomlDoc = self.__generatePyprojectNew(pyprojectOrigPath, requirements)

        with pyprojectNewPath.open('w') as t:
            t.write(tomlDoc.as_string())

        self.__buildWheel(pyprojectOrigPath, pyprojectNewPath, basePath)

    def __readRequirements(self, requirementsPath: Path):
        with requirementsPath.open('r') as f:
            lines = f.readlines()

            return list(map(self.__requirementsLineConverter.parse, lines))

    def __generatePyprojectNew(self, pyprojectOrigPath: Path, requirements: list) -> TOMLDocument:
        with pyprojectOrigPath.open('r') as t:
            tomlDoc = tomlkit.parse(t.read())

            dependencies = tomlDoc['tool']['poetry']['dependencies']

            if 'python' not in dependencies:
                raise Exception('"python" must be defined in [tool.poetry.dependencies]')

            newDependencies = table()
            newDependencies.add('python', dependencies['python'])

            for requirement in requirements:
                newDependencies.add(*requirement)

            tomlDoc['tool']['poetry']['dependencies'] = newDependencies

        return tomlDoc

    def __buildWheel(self, pyprojectOrigPath: Path, pyprojectNewPath: Path, basePath: Path):
        pyprojectDist = basePath.joinpath('dist/pyproject.toml')
        pyprojectBakPath = basePath.joinpath('pyproject.toml.bak')

        pyprojectOrigPath.rename(pyprojectBakPath)
        pyprojectNewPath.rename(pyprojectOrigPath)

        try:
            subprocess.run('poetry build --format wheel', check=True, cwd=str(basePath), shell=True)
        except BaseException: # pylint: disable = broad-except
            pass
        finally:
            pyprojectOrigPath.replace(pyprojectDist)
            pyprojectBakPath.rename(pyprojectOrigPath)
