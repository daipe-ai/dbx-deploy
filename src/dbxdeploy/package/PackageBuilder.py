import subprocess
from typing import List
import tomlkit
from tomlkit import table
from tomlkit.toml_document import TOMLDocument
from tomlkit.items import Table
from pathlib import Path
from dbxdeploy.package.Lock2PyprojectConverter import Lock2PyprojectConverter

class PackageBuilder:

    def __init__(
        self,
        lock2PyprojectConverter: Lock2PyprojectConverter,
    ):
        self.__lock2PyprojectConverter = lock2PyprojectConverter

    def build(self, basePath: Path):
        basePath.joinpath('dist').mkdir(exist_ok=True)

        lockfilePath = basePath.joinpath('poetry.lock')
        pyprojectOrigPath = basePath.joinpath('pyproject.toml')
        pyprojectNewPath = basePath.joinpath('pyproject.toml.new')

        mainDependencies = self.__loadMainDependencies(lockfilePath)
        tomlDoc = self.__generatePyprojectNew(pyprojectOrigPath, mainDependencies)

        with pyprojectNewPath.open('w') as t:
            t.write(tomlDoc.as_string())

        self.__buildWheel(pyprojectOrigPath, pyprojectNewPath, basePath)

    def __loadMainDependencies(self, lockfilePath: Path) -> List[Table]:
        with lockfilePath.open('r') as f:
            config = tomlkit.parse(f.read())

            return [package for package in config['package'] if package['category'] == 'main' and package['name']]

    def __generatePyprojectNew(self, pyprojectOrigPath: Path, mainDependencies: List[Table]) -> TOMLDocument:
        with pyprojectOrigPath.open('r') as t:
            tomlDoc = tomlkit.parse(t.read())

            dependencies = tomlDoc['tool']['poetry']['dependencies']

            if 'python' not in dependencies:
                raise Exception('"python" must be defined in [tool.poetry.dependencies]')

            newDependencies = table()
            newDependencies.add('python', dependencies['python'])

            for mainDependency in mainDependencies:
                packageName, packageDefinition = self.__lock2PyprojectConverter.convert(mainDependency)
                newDependencies.add(packageName, packageDefinition)

            tomlDoc['tool']['poetry']['dependencies'] = newDependencies
            del tomlDoc['tool']['poetry']['dev-dependencies']

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
