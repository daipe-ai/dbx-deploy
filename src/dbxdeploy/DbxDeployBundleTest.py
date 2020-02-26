import unittest
from consolebundle.ConsoleBundle import ConsoleBundle
from injecta.testing.servicesTester import testServices
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.package.pathResolver import resolvePath
from typing import List
from pyfony.PyfonyBundle import PyfonyBundle
from pyfony.kernel.BaseKernel import BaseKernel
from pyfonybundles.Bundle import Bundle
from dbxdeploy.DbxDeployBundle import DbxDeployBundle

class DbxDeployBundleTest(unittest.TestCase):

    def test_init(self):
        class Kernel(BaseKernel):

            def _registerBundles(self) -> List[Bundle]:
                return [
                    PyfonyBundle(),
                    ConsoleBundle(),
                    DbxDeployBundle()
                ]

        kernel = Kernel(
            'test',
            resolvePath('dbxdeploy') + '/DbxDeployBundleTest',
            YamlConfigReader()
        )

        container = kernel.initContainer()

        testServices(container)

if __name__ == '__main__':
    unittest.main()
