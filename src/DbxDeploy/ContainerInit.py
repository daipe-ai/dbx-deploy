from Injecta.YamlDefinitionsReaderParser import YamlDefinitionsReaderParser
from Injecta.ContainerInitializer import ContainerInitializer
from DbxDeploy.getLibRoot import getLibRoot
from pathlib import Path
import yaml
from box import Box

class ContainerInit:

    def init(init, deployYamlPath: Path):
        if deployYamlPath.is_file() is False:
            raise Exception('Config {} does not exist, create it from deploy.yaml.dist'.format(deployYamlPath))

        with deployYamlPath.open('r', encoding='utf-8') as f:
            yamlConfig = yaml.safe_load(f.read())
            f.close()

        if 'projectBasePath' in yamlConfig['databricks']:
            yamlConfig['databricks']['projectBasePath'] = Path(yamlConfig['databricks']['projectBasePath'])
        else:
            yamlConfig['databricks']['projectBasePath'] = deployYamlPath.parent

        return ContainerInitializer().init(
            Box(yamlConfig),
            YamlDefinitionsReaderParser().readAndParse(getLibRoot() + '/services.yaml')
        )
