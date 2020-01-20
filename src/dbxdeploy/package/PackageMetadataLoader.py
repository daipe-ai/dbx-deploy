from pathlib import Path
import tomlkit
from datetime import datetime
from dbxdeploy.package.PackageMetadata import PackageMetadata
from dbxdeploy.string.RandomStringGenerator import RandomStringGenerator

class PackageMetadataLoader:

    def load(self, projectBasePath: Path) -> PackageMetadata:
        pyprojectPath = projectBasePath.joinpath('pyproject.toml')

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
            )
