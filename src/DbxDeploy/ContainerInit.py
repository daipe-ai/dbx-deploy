from pathlib import Path
from DbxDeploy.Git.CurrentBranchResolver import CurrentBranchResolver
from DbxDeploy.LibRoot import getLibRoot
from Injecta.Config.YamlConfigReader import YamlConfigReader
from Injecta.Config.ConfigLoader import ConfigLoader
from Injecta.Config.ConfigMerger import ConfigMerger
from Injecta.ContainerInitializer import ContainerInitializer
from Injecta.Service.ServiceDefinitionsParser import ServiceDefinitionsParser
from Injecta.Parameter.ParametersParser import ParametersParser
from Injecta.ContainerInterface import ContainerInterface

class ContainerInit:

    def __init__(self, currentBranchResolver: CurrentBranchResolver):
        self.__currentBranchResolver = currentBranchResolver

    def init(self, deployYamlPath: Path) -> ContainerInterface:
        if deployYamlPath.is_file() is False:
            raise Exception('Config {} does not exist, create it from deploy.yaml.dist'.format(deployYamlPath))

        deployRawConfig = ConfigLoader().load(deployYamlPath)
        rawYamlConfig = YamlConfigReader().read(getLibRoot() + '/_config/config.yaml')

        if 'parameters' in rawYamlConfig:
            rawYamlConfig['parameters'] = ConfigMerger().merge(rawYamlConfig['parameters'], deployRawConfig)
        else:
            rawYamlConfig['parameters'] = deployRawConfig

        if 'projectBasePath' not in rawYamlConfig['parameters']['databricks']:
            rawYamlConfig['parameters']['databricks']['projectBasePath'] = str(deployYamlPath.parent)

        serviceDefinitions = ServiceDefinitionsParser().parse(rawYamlConfig['services'])
        parameters = ParametersParser().parse(rawYamlConfig['parameters'], {
            'currentBranch': self.__currentBranchResolver.resolve()
        })

        return ContainerInitializer().init(parameters, serviceDefinitions)
