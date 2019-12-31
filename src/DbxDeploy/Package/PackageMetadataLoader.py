from pathlib import Path
import tomlkit
from DbxDeploy.Package.PackageMetadata import PackageMetadata
from datetime import datetime
from DbxDeploy.String.RandomStringGenerator import RandomStringGenerator

class PackageMetadataLoader:

    def load(self, projectBasePath: Path) -> PackageMetadata:
        pyprojectPath = projectBasePath.joinpath('pyproject.toml')

        with pyprojectPath.open('r') as t:
            lock = tomlkit.parse(t.read())

            toolParams = lock['tool']['poetry']

            return PackageMetadata(
                str(toolParams['name']),
                float(str(toolParams['version'])),
                datetime.now(),
                RandomStringGenerator().generate(10),
            )
