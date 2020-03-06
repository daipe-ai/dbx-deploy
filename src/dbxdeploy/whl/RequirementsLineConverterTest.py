import unittest
from dbxdeploy.whl.RequirementsLineConverter import RequirementsLineConverter

class RequirementsLineConverterTest(unittest.TestCase):

    def setUp(self):
        self.__requirementsLineConverter = RequirementsLineConverter()

    def test_basic(self):
        result = self.__requirementsLineConverter.parse('appnope==0.1.0')

        self.assertEqual(['appnope', '0.1.0'], result)

    def test_withSysPlatform(self):
        result = self.__requirementsLineConverter.parse('appnope==0.1.0; sys_platform == "darwin"')

        self.assertEqual(['appnope', {'version': '0.1.0', 'markers': 'sys_platform == "darwin"'}], result)

    def test_multipleConditions(self):
        result = self.__requirementsLineConverter.parse('pywin32==227; sys_platform == "win32" and python_version >= "3.6" or sys_platform == "win32"')

        self.assertEqual(['pywin32', {'version': '227', 'markers': 'sys_platform == "win32" and python_version >= "3.6" or sys_platform == "win32"'}], result)

if __name__ == '__main__':
    unittest.main()
