import tomlkit
from tomlkit.toml_document import TOMLDocument
from tomlkit.items import Table
from typing import List
from pathlib import Path


class PackageIndexResolver:
    def __init__(
        self,
        project_base_dir: Path,
    ):
        self.__project_base_dir = project_base_dir

    def get_default_index(self) -> Table:
        toml_doc = self.__load_pyproject_toml()

        if "source" not in toml_doc["tool"]["poetry"]:
            return None

        sources = toml_doc["tool"]["poetry"]["source"]

        for source in sources:
            if source.get("default") is True:
                return source

        return None

    def get_secondary_indexes(self) -> List[Table]:
        toml_doc = self.__load_pyproject_toml()

        if "source" not in toml_doc["tool"]["poetry"]:
            return None

        sources = toml_doc["tool"]["poetry"]["source"]
        extra_indexes = []

        for source in sources:
            if source.get("secondary") is True:
                extra_indexes.append(source)

        if len(extra_indexes) > 0:
            return extra_indexes

        return None

    def has_default_index(self) -> bool:
        return self.get_default_index() is not None

    def has_secondary_indexes(self) -> bool:
        return self.get_secondary_indexes() is not None

    def __load_pyproject_toml(self) -> TOMLDocument:
        pyproject_path = self.__project_base_dir.joinpath("pyproject.toml")

        with pyproject_path.open("r") as f:
            toml_doc = tomlkit.parse(f.read())

        return toml_doc
