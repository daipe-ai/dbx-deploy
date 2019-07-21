from abc import ABC
from pathlib import Path
from DbxDeploy.Whl.PackageMetadata import PackageMetadata

class SetupInterface(ABC):
    pass

    def build(self, projectBasePath: Path) -> PackageMetadata:
        pass
