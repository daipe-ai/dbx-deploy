from pathlib import Path
from argparse import Namespace
from dbxdeploy.package.PackageBuilder import PackageBuilder
from consolebundle.ConsoleCommand import ConsoleCommand


class MasterPackageBuilder(ConsoleCommand):
    def __init__(
        self,
        projectBaseDir: Path,
        packageBuilder: PackageBuilder,
    ):
        self.__projectBaseDir = projectBaseDir
        self.__packageBuilder = packageBuilder

    def getCommand(self) -> str:
        return "dbx:build-master-package"

    def getDescription(self):
        return "Build the master package"

    def run(self, inputArgs: Namespace):
        self.__packageBuilder.build(self.__projectBaseDir)
