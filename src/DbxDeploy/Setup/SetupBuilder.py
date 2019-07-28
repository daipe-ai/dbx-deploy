from DbxDeploy.Setup.SetupInterface import SetupInterface
from pathlib import Path
from DbxDeploy.Whl.PackageMetadata import PackageMetadata
import sys

class SetupBuilder:

    def build(self, setup: SetupInterface, projectBasePath: Path) -> PackageMetadata:
        projectBasePath.joinpath('dist').mkdir(exist_ok=True)

        logFilePath = projectBasePath.joinpath('dist/build.log')
        errFilePath = projectBasePath.joinpath('dist/build.err')

        origStdout = sys.stdout
        origStderr = sys.stderr

        logFile = logFilePath.open('w', encoding='utf-8')
        errFile = errFilePath.open('w', encoding='utf-8')
        sys.stdout = logFile
        sys.stderr = errFile

        packageMetadata = setup.build(projectBasePath)

        logFile.close()
        errFile.close()

        sys.stdout = origStdout
        sys.stderr = origStderr

        return packageMetadata
