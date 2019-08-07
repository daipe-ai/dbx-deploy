from Injecta.YamlDefinitionsReaderParser import YamlDefinitionsReaderParser
from Injecta.ContainerInitializer import ContainerInitializer
from Injecta.ContainerInterface import ContainerInterface
from Injecta.Config.YamlConfigReader import YamlConfigReader
from DbxDeploy.getLibRoot import getLibRoot
from pathlib import Path
from box import Box

class ContainerInit:

    def init(init, deployYamlPath: Path) -> ContainerInterface:
        if deployYamlPath.is_file() is False:
            raise Exception('Config {} does not exist, create it from deploy.yaml.dist'.format(deployYamlPath))

        yamlConfig = YamlConfigReader().read(str(deployYamlPath))

        if 'projectBasePath' in yamlConfig['databricks']:
            yamlConfig['databricks']['projectBasePath'] = Path(yamlConfig['databricks']['projectBasePath'])
        else:
            yamlConfig['databricks']['projectBasePath'] = deployYamlPath.parent

        return ContainerInitializer().init(
            Box(yamlConfig),
            YamlDefinitionsReaderParser().readAndParse(getLibRoot() + '/services.yaml')
        )
