from abc import ABC
from pathlib import Path
from DbxDeploy.Setup.PackageMetadata import PackageMetadata
from setuptools.dist import Distribution

class SetupInterface(ABC):

    def getPackageMetadata(self) -> PackageMetadata:
        pass

    def build(self, projectBasePath: Path) -> Distribution:
        pass
