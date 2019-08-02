from DbxDeploy.ContainerInit import ContainerInit
import sys
from pathlib import Path
from DbxDeploy.Deployer import Deployer
import asyncio

class DeployerCommand:

    @classmethod
    def run(cls):
        if len(sys.argv) < 1:
            raise Exception('Path to deployment YAML config not provided (argument #1)')

        deployYamlPath = Path(sys.argv[1])

        container = ContainerInit().init(deployYamlPath)

        deployer = container.get(Deployer) # type: Deployer

        loop = asyncio.get_event_loop()
        loop.run_until_complete(deployer.deploy())
