from pathlib import Path
from argparse import Namespace
from dbxdeploy.package.PackageMetadataLoader import PackageMetadataLoader
from dbxdeploy.package.PackageDeployer import PackageDeployer
from consolebundle.ConsoleCommand import ConsoleCommand


class MasterPackageDeployer(ConsoleCommand):

    def __init__(
        self,
        projectBaseDir: Path,
        packageMetadataLoader: PackageMetadataLoader,
        packageDeployer: PackageDeployer,
    ):
        self.__projectBaseDir = projectBaseDir
        self.__packageMetadataLoader = packageMetadataLoader
        self.__packageDeployer = packageDeployer

    def getCommand(self) -> str:
        return 'dbx:deploy-master-package'

    def getDescription(self):
        return 'Deploy WHL to DBX'

    def run(self, inputArgs: Namespace):
        packageMetadata = self.__packageMetadataLoader.load(self.__projectBaseDir)

        self.__packageDeployer.deploy(packageMetadata)
