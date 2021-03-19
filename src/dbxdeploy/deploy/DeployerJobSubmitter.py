from dbxdeploy.job.NotebookKiller import NotebookKiller
from dbxdeploy.notebook.NotebooksLocator import NotebooksLocator
from dbxdeploy.package.PackageMetadata import PackageMetadata
from dbxdeploy.package.PackageMetadataLoader import PackageMetadataLoader
from dbxdeploy.package.PackageDeployer import PackageDeployer
from dbxdeploy.notebook.NotebooksDeployer import NotebooksDeployer
from dbxdeploy.job.JobSubmitter import JobSubmitter
from pathlib import Path, PurePosixPath
import asyncio


class DeployerJobSubmitter:
    def __init__(
        self,
        project_base_dir: Path,
        package_metadata_loader: PackageMetadataLoader,
        notebook_killer: NotebookKiller,
        notebooks_deployer: NotebooksDeployer,
        package_deployer: PackageDeployer,
        job_submitter: JobSubmitter,
        notebooks_locator: NotebooksLocator,
    ):
        self.__project_base_dir = project_base_dir
        self.__package_metadata_loader = package_metadata_loader
        self.__notebook_killer = notebook_killer
        self.__notebooks_deployer = notebooks_deployer
        self.__package_deployer = package_deployer
        self.__job_submitter = job_submitter
        self.__notebooks_locator = notebooks_locator

    async def deploy_and_submit_job(self, notebook_path: PurePosixPath):
        package_metadata = self.__package_metadata_loader.load(self.__project_base_dir)

        def deploy_root(package_metadata: PackageMetadata):
            notebooks = self.__notebooks_locator.locate()
            self.__notebooks_deployer.deploy(package_metadata, notebooks)

        loop = asyncio.get_event_loop()

        notebook_killer_future = loop.run_in_executor(None, self.__notebook_killer.kill_if_running, notebook_path, package_metadata)
        package_deploy_future = loop.run_in_executor(None, self.__package_deployer.deploy, package_metadata)
        dbc_deploy_future = loop.run_in_executor(None, deploy_root, package_metadata)

        await notebook_killer_future
        await package_deploy_future
        await dbc_deploy_future

        self.__job_submitter.submit(notebook_path, package_metadata)
