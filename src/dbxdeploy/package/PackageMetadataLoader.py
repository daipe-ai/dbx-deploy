from pathlib import Path
import tomlkit
from datetime import datetime
from dbxdeploy.package.PackageMetadata import PackageMetadata
from dbxdeploy.package.PackageDependencyLoader import PackageDependencyLoader
from dbxdeploy.string.RandomStringGenerator import RandomStringGenerator


class PackageMetadataLoader:
    def __init__(
        self,
        package_dependency_loader: PackageDependencyLoader,
    ):
        self.__package_dependency_loader = package_dependency_loader

    def load(self, project_base_dir: Path) -> PackageMetadata:
        pyproject_path = project_base_dir.joinpath("pyproject.toml")

        with pyproject_path.open("r") as t:
            lock = tomlkit.parse(t.read())

            tool_params = lock["tool"]["poetry"]

            package_name = str(tool_params["name"])
            package_version = str(tool_params["version"])

            return PackageMetadata(
                package_name,
                package_version,
                datetime.now(),
                RandomStringGenerator().generate(10),
                self.__package_dependency_loader.load(project_base_dir),
            )
