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

    def test_gitSsh(self):
        result = self.__requirementsLineConverter.parse('-e git+git@github.com:myaccount/myrepo.git@master#egg=my-package-name')

        self.assertEqual(['my-package-name', {'git': 'git@github.com:myaccount/myrepo.git', 'rev': 'master'}], result)

    def test_gitHttpsOld(self):
        result = self.__requirementsLineConverter.parse('-e git+https://github.com/myaccount/myrepo.git@82f1bb9de9665918c262465e72e872e4f744112c#egg=my-package-name')

        self.assertEqual(['my-package-name', {'git': 'https://github.com/myaccount/myrepo.git', 'rev': '82f1bb9de9665918c262465e72e872e4f744112c'}], result)

    def test_gitHttpsWithTokenOld(self):
        result = self.__requirementsLineConverter.parse('-e git+https://sometoken@github.com/myaccount/myrepo.git@82f1bb9de9665918c262465e72e872e4f744112c#egg=my-package-name')

        self.assertEqual(['my-package-name', {'git': 'https://sometoken@github.com/myaccount/myrepo.git', 'rev': '82f1bb9de9665918c262465e72e872e4f744112c'}], result)

    def test_gitHttps(self):
        result = self.__requirementsLineConverter.parse('my-package-name @ git+https://sometoken@github.com/myaccount/myrepo.git@master#egg=my-package-name')

        self.assertEqual(['my-package-name', {'git': 'https://sometoken@github.com/myaccount/myrepo.git', 'rev': 'master'}], result)

    def test_gitHttps_noEgg(self):
        result = self.__requirementsLineConverter.parse('my-package-name @ git+https://sometoken@github.com/myaccount/myrepo.git@master')

        self.assertEqual(['my-package-name', {'git': 'https://sometoken@github.com/myaccount/myrepo.git', 'rev': 'master'}], result)

    def test_gitHttpsWithToken(self):
        result = self.__requirementsLineConverter.parse('my-package-name @ git+https://github.com/myaccount/myrepo.git@master#egg=my-package-name')

        self.assertEqual(['my-package-name', {'git': 'https://github.com/myaccount/myrepo.git', 'rev': 'master'}], result)

    def test_gitHttpsWithToken_noEgg(self):
        result = self.__requirementsLineConverter.parse('my-package-name @ git+https://github.com/myaccount/myrepo.git@master')

        self.assertEqual(['my-package-name', {'git': 'https://github.com/myaccount/myrepo.git', 'rev': 'master'}], result)

if __name__ == '__main__':
    unittest.main()
