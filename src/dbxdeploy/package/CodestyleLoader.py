from pathlib import Path

import tomlkit
from tomlkit.toml_document import TOMLDocument


class CodestyleLoader:
    def __init__(
        self,
        package_base_dir: Path,
    ):
        self.__package_base_dir = package_base_dir

    def get_flake8(self):
        toml_doc = self.__load_pyproject_toml()
        flake8_cmd = str(toml_doc["tool"]["poe"]["tasks"]["flake8"])
        flake8_options = flake8_cmd.split()[1:3]
        flake8_options = " ".join([f"--{opt[2:].replace('=', ' ').replace('-', '_')}" for opt in flake8_options])

        return (
            "# %turn_on_flake8\n"
            "import IPython\n"
            "ipy = IPython.get_ipython()\n"
            "ipy.run_line_magic('load_ext', 'pycodestyle_magic')\n"
            f"ipy.run_line_magic('flake8_on', '{flake8_options}')"
        )

    def __load_pyproject_toml(self) -> TOMLDocument:
        pyproject_path = self.__package_base_dir.joinpath("pyproject.toml")

        with pyproject_path.open("r") as f:
            toml_doc = tomlkit.parse(f.read())

        return toml_doc
