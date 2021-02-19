from pathlib import Path
import tomlkit
from datetime import datetime
from dbxdeploy.package.PackageMetadata import PackageMetadata
from dbxdeploy.package.PackageDependencyLoader import PackageDependencyLoader
from dbxdeploy.string.RandomStringGenerator import RandomStringGenerator

class PackageMetadataLoader:

    def __init__(
        self,
        packageDependencyLoader: PackageDependencyLoader,
    ):
        self.__packageDependencyLoader = packageDependencyLoader

    def load(self, projectBaseDir: Path) -> PackageMetadata:
        pyprojectPath = projectBaseDir.joinpath('pyproject.toml')

        with pyprojectPath.open('r') as t:
            lock = tomlkit.parse(t.read())

            toolParams = lock['tool']['poetry']

            packageName = str(toolParams['name'])
            packageVersion = float(str(toolParams['version']))

            return PackageMetadata(
                packageName,
                packageVersion,
                datetime.now(),
                RandomStringGenerator().generate(10),
                self.__packageDependencyLoader.load(projectBaseDir)
            )
