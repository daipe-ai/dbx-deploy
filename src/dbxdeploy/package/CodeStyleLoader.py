from typing import List, Dict

import tomlkit
from pyfonycore.pyproject import read, get_path
from pathlib import Path

from tomlkit.toml_document import TOMLDocument


class CodeStyleLoader:
    def __init__(
        self,
        package_base_dir: Path,
    ):
        self.__package_base_dir = package_base_dir

    def get_codestyle_install_command(self) -> str:
        versions = self.__get_versions(["flake8", "pycodestyle-magic"])

        return (
            f"# {self.get_setup_command()}\n"
            "import IPython  # noqa E402\n"
            f"IPython.get_ipython().run_line_magic('pip', 'install flake8=={versions['flake8']} pycodestyle_magic=={versions['pycodestyle-magic']}')\n"
        )

    def get_codestyle_setup_command(self) -> str:
        toml_doc = self.__load_pyproject_toml()
        flake8_cmd = toml_doc["tool"]["poe"]["tasks"]["flake8"]
        flake8_options = str(flake8_cmd).split()
        flake8_options = " ".join([f"--{opt[2:].replace('=', ' ').replace('-', '_')}" for opt in flake8_options if opt.startswith("--")])

        return (
            "import IPython  # noqa E402\n"
            f"ipy = IPython.get_ipython()\n"
            "ipy.run_line_magic('load_ext', 'pycodestyle_magic')\n"
            f"ipy.run_line_magic('flake8_on', '{flake8_options}')"
        )

    def get_setup_command(self) -> str:
        return "%flake8_setup"

    def __load_pyproject_toml(self) -> TOMLDocument:
        return read(get_path(self.__package_base_dir))

    def __get_versions(self, packages: List[str]) -> Dict[str, str]:
        lockfile_path = self.__package_base_dir.joinpath("poetry.lock")
        with lockfile_path.open("r") as f:
            config = tomlkit.parse(f.read())

        return {
            package["name"]: package["version"]
            for package in config["package"]
            if package["category"] == "dev" and package["name"] in packages
        }
