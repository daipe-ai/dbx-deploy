from argparse import Namespace
from pathlib import Path
from dbxdeploy.package.PackageBuilder import PackageBuilder
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.package.PackageMetadataLoader import PackageMetadataLoader

class MasterPackageBuilder(ConsoleCommand):
    def __init__(
        self,
        packageMetadataLoader: PackageMetadataLoader,
        packageBuilder: PackageBuilder,
    ):
        self.__packageMetadataLoader = packageMetadataLoader
        self.__packageBuilder = packageBuilder

    def getCommand(self) -> str:
        return "dbx:build-master-package"

    def getDescription(self):
        return "Build the master package"

    def run(self, inputArgs: Namespace):
        projectBaseDir = Path.cwd()
        packageMetadata = self.__packageMetadataLoader.load(projectBaseDir)

        self.__packageBuilder.build(projectBaseDir, packageMetadata.getPackageFilename())
