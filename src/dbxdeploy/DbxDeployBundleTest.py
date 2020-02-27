import unittest
from injecta.testing.servicesTester import testServices
from dbxdeploy.containerInit import initContainer

class DbxDeployBundleTest(unittest.TestCase):

    def test_init(self):
        container = initContainer('test')

        testServices(container)

if __name__ == '__main__':
    unittest.main()
