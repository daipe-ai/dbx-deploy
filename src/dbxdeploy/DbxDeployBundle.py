import os
from typing import List
from injecta.bundle.Bundle import Bundle
from injecta.config.ConfigMerger import ConfigMerger
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.definition.Definition import Definition
from injecta.bundle.definitionsPreparerFactory import create as createDefinitionsPreparer

class DbxDeployBundle(Bundle):

    def __init__(self):
        self.__configReader = YamlConfigReader()
        self.__definitionsPreparer = createDefinitionsPreparer()
        self.__configMerger = ConfigMerger()

    def modifyDefinitions(self, definitions: List[Definition]):
        currentDir = os.path.dirname(os.path.abspath(__file__))
        config = self.__configReader.read(currentDir + '/_config/services.yaml')

        newDefinitions = self.__definitionsPreparer.prepare(config['services'])

        return definitions + newDefinitions

    def modifyRawConfig(self, rawConfig: dict) -> dict:
        defaultConfig = {
            'browser': {
                'path': 'c:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
                'arguments': ['-d', '{runUrl}'],
            },
            'databricks': {
                'projectRoot': '/{currentBranch}',
                'whlBaseDir': 'dbfs:/FileStore/jars',
            }
        }

        dbxDeployConfig = self.__configMerger.merge(defaultConfig, rawConfig['dbxdeploy'])

        rawConfig['parameters'] = self.__configMerger.merge(rawConfig['parameters'], {
            'dbxdeploy': dbxDeployConfig,
        })

        return rawConfig
