from dbxdeploy.deploy.CurrentAndReleaseDeployer import CurrentAndReleaseDeployer
from dbxdeploy.package.PackageMetadataLoader import PackageMetadataLoader
from dbxdeploy.package.PackageDeployer import PackageDeployer
from pathlib import Path
import asyncio


class Deployer:
    def __init__(
        self,
        project_base_dir: Path,
        package_metadata_loader: PackageMetadataLoader,
        current_and_release_deployer: CurrentAndReleaseDeployer,
        package_deployer: PackageDeployer,
    ):
        self.__project_base_dir = project_base_dir
        self.__package_metadata_loader = package_metadata_loader
        self.__current_and_release_deployer = current_and_release_deployer
        self.__package_deployer = package_deployer

    async def deploy(self):
        package_metadata = self.__package_metadata_loader.load(self.__project_base_dir)

        loop = asyncio.get_event_loop()

        package_deploy_future = loop.run_in_executor(None, self.__package_deployer.deploy, package_metadata)
        dbc_deploy_future = loop.run_in_executor(None, self.__current_and_release_deployer.deploy, package_metadata)

        await package_deploy_future
        await dbc_deploy_future
