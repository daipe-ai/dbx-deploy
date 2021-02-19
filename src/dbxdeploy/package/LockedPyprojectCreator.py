import tomlkit
from tomlkit import table
from tomlkit.toml_document import TOMLDocument
from pathlib import Path
from dbxdeploy.package.RequirementsLineConverter import RequirementsLineConverter
from dbxdeploy.package.RequirementsCreator import RequirementsCreator

class LockedPyprojectCreator:

    def __init__(
        self,
        requirementsLineConverter: RequirementsLineConverter,
        requirementsCreator: RequirementsCreator,
    ):
        self.__requirementsLineConverter = requirementsLineConverter
        self.__requirementsCreator = requirementsCreator

    def create(self, basePath: Path, pyprojectOrigPath: Path, pyprojectNewPath: Path):
        tomlDoc = self.getLockedPyprojectToml(basePath, pyprojectOrigPath)

        with pyprojectNewPath.open('w') as t:
            t.write(tomlDoc.as_string())

    def getLockedPyprojectToml(self, basePath: Path, pyprojectOrigPath: Path) -> TOMLDocument:
        mainDependencies = self.__loadMainDependencies(basePath)
        tomlDoc = self.__generatePyprojectNew(pyprojectOrigPath, mainDependencies)

        return tomlDoc

    def __loadMainDependencies(self, basePath: Path) -> list:
        requirements = self.__requirementsCreator.exportToString(basePath).splitlines()

        return list(map(self.__requirementsLineConverter.parse, requirements))

    def __generatePyprojectNew(self, pyprojectOrigPath: Path, requirements: list) -> TOMLDocument:
        with pyprojectOrigPath.open('r') as t:
            tomlDoc = tomlkit.parse(t.read())

            dependencies = tomlDoc['tool']['poetry']['dependencies']

            if 'python' not in dependencies:
                raise Exception('"python" must be defined in [tool.poetry.dependencies]')

            newDependencies = table()
            newDependencies.add('python', dependencies['python'])

            for requirement in requirements:
                if self.__isLinuxDependency(requirement):
                    newDependencies.add(*requirement)

            tomlDoc['tool']['poetry']['dependencies'] = newDependencies
            del tomlDoc['tool']['poetry']['dev-dependencies']

        return tomlDoc

    def __isLinuxDependency(self, requirement):
        markersPresent = isinstance(requirement[1], dict) and 'markers' in requirement[1]

        if not markersPresent:
            return True

        platformInfoPresent = 'sys_platform' in requirement[1]['markers'] or \
                              'platform_system' in requirement[1]['markers']

        if not platformInfoPresent:
            return True

        isLinuxDependency = 'sys_platform == "linux"' in requirement[1]['markers'] or \
                            'sys_platform == "linux2"' in requirement[1]['markers'] or \
                            'platform_system == "Linux"' in requirement[1]['markers']

        return isLinuxDependency
