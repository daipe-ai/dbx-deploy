from argparse import Namespace, ArgumentParser
from pathlib import Path
from dbxdeploy.package.DependencyBuilder import DependencyBuilder
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.package.PackageMetadataLoader import PackageMetadataLoader


class DependencyBuilderCommand(ConsoleCommand):
    def __init__(
        self,
        project_base_dir: Path,
        package_metadata_loader: PackageMetadataLoader,
        dependency_builder: DependencyBuilder,
    ):
        self.__project_base_dir = project_base_dir
        self.__package_metadata_loader = package_metadata_loader
        self.__dependency_builder = dependency_builder

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument("--dev", action="store_true")

    def get_command(self) -> str:
        return "dbx:build-dependencies"

    def get_description(self):
        return "Build linux dependencies on remote DBX cluster and then download them in local dependencies directory"

    def run(self, input_args: Namespace):
        package_metadata = self.__package_metadata_loader.load(self.__project_base_dir)

        self.__dependency_builder.build(self.__project_base_dir, package_metadata, dev_dependencies=input_args.dev)
