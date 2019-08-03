from DbxDeploy.ContainerInit import ContainerInit
import sys
from pathlib import Path
from DbxDeploy.DeployWithCleanup import DeployWithCleanup
import asyncio

class DeployWithCleanupCommand:

    @classmethod
    def run(cls):
        if len(sys.argv) < 1:
            raise Exception('Path to deployment YAML config not provided (argument #1)')

        deployYamlPath = Path(sys.argv[1])

        container = ContainerInit().init(deployYamlPath)

        deployWithCleanup = container.get(DeployWithCleanup) # type: DeployWithCleanup

        loop = asyncio.get_event_loop()
        loop.run_until_complete(deployWithCleanup.deploy())
