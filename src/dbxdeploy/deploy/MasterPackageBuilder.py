from argparse import Namespace
from pathlib import Path
from dbxdeploy.package.PackageBuilder import PackageBuilder
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.package.PackageMetadataLoader import PackageMetadataLoader


class MasterPackageBuilder(ConsoleCommand):
    def __init__(
        self,
        package_metadata_loader: PackageMetadataLoader,
        package_builder: PackageBuilder,
    ):
        self.__package_metadata_loader = package_metadata_loader
        self.__package_builder = package_builder

    def get_command(self) -> str:
        return "dbx:build-master-package"

    def get_description(self):
        return "Build the master package"

    def run(self, input_args: Namespace):
        project_base_dir = Path.cwd()
        package_metadata = self.__package_metadata_loader.load(project_base_dir)

        self.__package_builder.build(project_base_dir, package_metadata)
