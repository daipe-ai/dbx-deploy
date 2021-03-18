import unittest
from pyfonycore.bootstrap import bootstrapped_container
from dbxdeploy.dbc.CommandConverter import CommandConverter


class CommandConverterTest(unittest.TestCase):
    def setUp(self):
        container = bootstrapped_container.init("test")

        self.__command_converter = container.get(CommandConverter)  # type: CommandConverter

    def test_python_code(self):
        self.__test_command(
            'print("Hello world")',
            'print("Hello world")',
        )

    def test_python_code_multi_line_with_title(self):
        self.__test_command(
            'print("Hello world")\n\na = 5',
            '# DBTITLE 1,My Command Title\nprint("Hello world")\n\na = 5',
            showCommandTitle=True,
            commandTitle="My Command Title",
        )

    def test_magic(self):
        self.__test_command("%sql SELECT * FROM test_table", "# MAGIC %sql SELECT * FROM test_table")

    def test_magic_multi_line_with_title(self):
        self.__test_command(
            "%sql\n\nSELECT * FROM test_table",
            "# DBTITLE 1,My Command Title\n# MAGIC %sql\n# MAGIC \n# MAGIC SELECT * FROM test_table",
            showCommandTitle=True,
            commandTitle="My Command Title",
        )

    def test_install_master_package_whl(self):
        self.__test_command(
            "# %install_master_package_whl\nimport IPython, os\nIPython.get_ipython().run_line_magic('pip', f'install /dbfs/FileStore/jars/myproject/2020-03-21_08-56-14_fhpxgwblvi/myproject-1.0-py3-none-any.whl')",
            "# MAGIC %install_master_package_whl",
        )

    def test_install_master_package_whl_with_title(self):
        self.__test_command(
            "# %install_master_package_whl\nimport IPython, os\nIPython.get_ipython().run_line_magic('pip', f'install /dbfs/FileStore/jars/myproject/2020-03-21_08-56-14_fhpxgwblvi/myproject-1.0-py3-none-any.whl')",
            "# DBTITLE 0,My Command Title\n# MAGIC %install_master_package_whl",
            showCommandTitle=False,
            commandTitle="My Command Title",
        )

    def __test_command(self, command_code: str, expected_line: str, **kwargs):
        command = {**{"command": command_code, "position": 1, "commandTitle": ""}, **kwargs}

        result = self.__command_converter.convert(command)

        self.assertEqual(result, expected_line)


if __name__ == "__main__":
    unittest.main()
