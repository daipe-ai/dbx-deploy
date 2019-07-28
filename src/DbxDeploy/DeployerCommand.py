from DbxDeploy.ContainerInit import ContainerInit
import sys
from pathlib import Path
from DbxDeploy.Deployer import Deployer

class DeployerCommand:

    @classmethod
    def run(cls):
        if len(sys.argv) < 1:
            raise Exception('Path to deployment YAML config not provided (argument #1)')

        deployYamlPath = Path(sys.argv[1])

        container = ContainerInit().init(deployYamlPath)

        deployer = container.get(Deployer) # type: Deployer
        deployer.deploy()
