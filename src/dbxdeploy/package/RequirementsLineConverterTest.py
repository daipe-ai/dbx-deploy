import unittest
from dbxdeploy.package.RequirementsLineConverter import RequirementsLineConverter


class RequirementsLineConverterTest(unittest.TestCase):
    def setUp(self):
        self.__requirements_line_converter = RequirementsLineConverter()

    def test_basic(self):
        result = self.__requirements_line_converter.parse("appnope==0.1.0")

        self.assertEqual(["appnope", "0.1.0"], result)

    def test_with_sys_platform(self):
        result = self.__requirements_line_converter.parse('appnope==0.1.0; sys_platform == "darwin"')

        self.assertEqual(["appnope", {"version": "0.1.0", "markers": 'sys_platform == "darwin"'}], result)

    def test_multiple_conditions(self):
        result = self.__requirements_line_converter.parse(
            'pywin32==227; sys_platform == "win32" and python_version >= "3.6" or sys_platform == "win32"'
        )

        self.assertEqual(
            ["pywin32", {"version": "227", "markers": 'sys_platform == "win32" and python_version >= "3.6" or sys_platform == "win32"'}],
            result,
        )

    def test_git_ssh(self):
        result = self.__requirements_line_converter.parse("-e git+git@github.com:myaccount/myrepo.git@master#egg=my-package-name")

        self.assertEqual(["my-package-name", {"git": "git@github.com:myaccount/myrepo.git", "rev": "master"}], result)

    def test_git_https_old(self):
        result = self.__requirements_line_converter.parse(
            "-e git+https://github.com/myaccount/myrepo.git@82f1bb9de9665918c262465e72e872e4f744112c#egg=my-package-name"
        )

        self.assertEqual(
            ["my-package-name", {"git": "https://github.com/myaccount/myrepo.git", "rev": "82f1bb9de9665918c262465e72e872e4f744112c"}],
            result,
        )

    def test_git_https_with_token_old(self):
        result = self.__requirements_line_converter.parse(
            "-e git+https://sometoken@github.com/myaccount/myrepo.git@82f1bb9de9665918c262465e72e872e4f744112c#egg=my-package-name"
        )

        self.assertEqual(
            [
                "my-package-name",
                {"git": "https://sometoken@github.com/myaccount/myrepo.git", "rev": "82f1bb9de9665918c262465e72e872e4f744112c"},
            ],
            result,
        )

    def test_git_https(self):
        result = self.__requirements_line_converter.parse(
            "my-package-name @ git+https://sometoken@github.com/myaccount/myrepo.git@master#egg=my-package-name"
        )

        self.assertEqual(["my-package-name", {"git": "https://sometoken@github.com/myaccount/myrepo.git", "rev": "master"}], result)

    def test_git_https_no_egg(self):
        result = self.__requirements_line_converter.parse("my-package-name @ git+https://sometoken@github.com/myaccount/myrepo.git@master")

        self.assertEqual(["my-package-name", {"git": "https://sometoken@github.com/myaccount/myrepo.git", "rev": "master"}], result)

    def test_git_https_with_token(self):
        result = self.__requirements_line_converter.parse(
            "my-package-name @ git+https://github.com/myaccount/myrepo.git@master#egg=my-package-name"
        )

        self.assertEqual(["my-package-name", {"git": "https://github.com/myaccount/myrepo.git", "rev": "master"}], result)

    def test_git_https_with_token_no_egg(self):
        result = self.__requirements_line_converter.parse("my-package-name @ git+https://github.com/myaccount/myrepo.git@master")

        self.assertEqual(["my-package-name", {"git": "https://github.com/myaccount/myrepo.git", "rev": "master"}], result)

    def test_local_windows_file(self):
        result = self.__requirements_line_converter.parse(
            "typed-ast @ file:///C:/dependencies/local/typed_ast-1.4.2-cp37-cp37m-win_amd64.whl"
        )

        self.assertEqual(["typed-ast", "1.4.2"], result)

    def test_local_windows_file_with_markers(self):
        result = self.__requirements_line_converter.parse(
            'zipp @ file:///C:/dependencies/local/zipp-3.4.0-py3-none-any.whl; python_version >= "3.6"'
        )

        self.assertEqual(["zipp", {"version": "3.4.0", "markers": 'python_version >= "3.6"'}], result)

    def test_local_linux_file(self):
        result = self.__requirements_line_converter.parse(
            "typed-ast @ file:///home/user/work/project/dependencies/local/typed_ast-1.4.2-cp37-cp37m-win_amd64.whl"
        )

        self.assertEqual(["typed-ast", "1.4.2"], result)

    def test_local_linux_file_with_markers(self):
        result = self.__requirements_line_converter.parse(
            'zipp @ file:///home/user/work/project/local/zipp-3.4.0-py3-none-any.whl; python_version >= "3.6"'
        )

        self.assertEqual(["zipp", {"version": "3.4.0", "markers": 'python_version >= "3.6"'}], result)


if __name__ == "__main__":
    unittest.main()
