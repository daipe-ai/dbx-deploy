from Injecta.YamlDefinitionsReaderParser import YamlDefinitionsReaderParser
from Injecta.ContainerInitializer import ContainerInitializer
from DbxDeploy.getLibRoot import getLibRoot
import sys
from pathlib import Path
import yaml
from box import Box
from DbxDeploy.Deployer import Deployer

class DeployerCommand:

    @classmethod
    def run(cls):
        projectBasePath = Path(sys.argv[1])

        if projectBasePath.is_dir() is False:
            raise Exception('Argument #1 must be project base directory')

        requirementsFilePath = Path(sys.argv[2])

        if requirementsFilePath.is_file() is False:
            raise Exception('Requirements file path is not valid')

        deployConfigPath = projectBasePath.joinpath(Path('deploy.yaml'))

        if deployConfigPath.is_file() is False:
            raise Exception('Config {} does not exist'.format(deployConfigPath))

        with open(str(deployConfigPath), 'r', encoding='utf-8') as f:
            yamlConfig = yaml.safe_load(f.read())
            f.close()

        container = ContainerInitializer().init(
            Box(yamlConfig),
            YamlDefinitionsReaderParser().readAndParse(getLibRoot() + '/services.yaml')
        )

        deployer = container.get(Deployer)
        deployer.deploy(projectBasePath, requirementsFilePath)
