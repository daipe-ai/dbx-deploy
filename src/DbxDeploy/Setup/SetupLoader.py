from DbxDeploy.Setup.SetupInterface import SetupInterface
import importlib.util
from pathlib import Path

class SetupLoader:

    def load(self, projectBasePath: Path) -> SetupInterface:
        spec = importlib.util.spec_from_file_location('build', '{}/setup.py'.format(projectBasePath))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module.Setup()
