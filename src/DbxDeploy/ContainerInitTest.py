import unittest
from pathlib import Path
from DbxDeploy.Git.CurrentBranchResolver import CurrentBranchResolver
from DbxDeploy.LibRoot import getLibRoot
from Injecta.Config.YamlConfigReader import YamlConfigReader

class FakeCurrentBranchResolver(CurrentBranchResolver):

    def resolve(self):
        return 'master'

class ContainerInitTest(unittest.TestCase):

    def test_init(self):
        from DbxDeploy.ContainerInit import ContainerInit

        deployYamlPath = Path(getLibRoot() + '/deploy.yaml.test')
        container = ContainerInit(FakeCurrentBranchResolver()).init(deployYamlPath)

        configPath = getLibRoot() + '/_config/config.yaml'
        rawYamlConfig = YamlConfigReader().read(configPath)

        for serviceName, serviceDefinition in rawYamlConfig['services'].items():
            container.get(serviceName)

if __name__ == '__main__':
    unittest.main()
