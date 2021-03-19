from pathlib import Path
from argparse import Namespace
from dbxdeploy.package.PackageMetadataLoader import PackageMetadataLoader
from dbxdeploy.package.PackageDeployer import PackageDeployer
from dbxdeploy.deploy.CurrentAndReleaseDeployer import CurrentAndReleaseDeployer
from consolebundle.ConsoleCommand import ConsoleCommand


class MasterPackageDeployer(ConsoleCommand):
    def __init__(
        self,
        project_base_dir: Path,
        package_metadata_loader: PackageMetadataLoader,
        package_deployer: PackageDeployer,
        current_and_release_deployer: CurrentAndReleaseDeployer,
    ):
        self.__project_base_dir = project_base_dir
        self.__package_metadata_loader = package_metadata_loader
        self.__package_deployer = package_deployer
        self.__current_and_release_deployer = current_and_release_deployer

    def get_command(self) -> str:
        return "dbx:deploy-master-package"

    def get_description(self):
        return "Deploy WHL to DBX"

    def run(self, input_args: Namespace):
        package_metadata = self.__package_metadata_loader.load(self.__project_base_dir)

        self.__package_deployer.deploy(package_metadata)
        self.__current_and_release_deployer.deploy_only_master_package_notebook(package_metadata)
