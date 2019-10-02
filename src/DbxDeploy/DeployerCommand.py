from DbxDeploy.ContainerInit import ContainerInit
from DbxDeploy.Git.CurrentBranchResolver import CurrentBranchResolver
import sys
from pathlib import Path
from DbxDeploy.Deployer import Deployer
import asyncio

class DeployerCommand:

    @classmethod
    def run(cls):
        if not sys.argv:
            raise Exception('Path to deployment YAML config not provided (argument #1)')

        deployYamlPath = Path(sys.argv[1])

        container = ContainerInit(CurrentBranchResolver()).init(deployYamlPath)

        deployer = container.get(Deployer) # type: Deployer

        loop = asyncio.get_event_loop()
        loop.run_until_complete(deployer.deploy())
