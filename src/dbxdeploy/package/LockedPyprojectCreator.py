from typing import List
import tomlkit
from tomlkit import table
from tomlkit.toml_document import TOMLDocument
from tomlkit.items import Table
from pathlib import Path
from dbxdeploy.package.Lock2PyprojectConverter import Lock2PyprojectConverter

class LockedPyprojectCreator:

    def __init__(
        self,
        lock2PyprojectConverter: Lock2PyprojectConverter,
    ):
        self.__lock2PyprojectConverter = lock2PyprojectConverter

    def create(self, lockfilePath: Path, pyprojectOrigPath: Path, pyprojectNewPath: Path):
        mainDependencies = self.__loadMainDependencies(lockfilePath)
        tomlDoc = self.__generatePyprojectNew(pyprojectOrigPath, mainDependencies)

        with pyprojectNewPath.open('w') as t:
            t.write(tomlDoc.as_string())

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
