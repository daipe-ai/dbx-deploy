from logging import Logger
from pathlib import Path
from dbxdeploy.cluster.ClusterRestarter import ClusterRestarter
from dbxdeploy.deploy.CurrentAndReleaseDeployer import CurrentAndReleaseDeployer
from dbxdeploy.job.JobsCreatorAndRunner import JobsCreatorAndRunner
from dbxdeploy.job.JobsDeleter import JobsDeleter
from dbxdeploy.notebook.Notebook import Notebook
from dbxdeploy.notebook.NotebooksLocator import NotebooksLocator
from dbxdeploy.package.PackageMetadataLoader import PackageMetadataLoader
from dbxdeploy.package.PackageDeployer import PackageDeployer
import asyncio
from dbxdeploy.deploy.TargetPathsResolver import TargetPathsResolver


class Releaser:
    def __init__(
        self,
        project_base_dir: Path,
        logger: Logger,
        target_paths_resolver: TargetPathsResolver,
        package_metadata_loader: PackageMetadataLoader,
        current_and_release_deployer: CurrentAndReleaseDeployer,
        package_deployer: PackageDeployer,
        cluster_restarter: ClusterRestarter,
        jobs_deleter: JobsDeleter,
        jobs_creator_and_runner: JobsCreatorAndRunner,
        notebooks_locator: NotebooksLocator,
    ):
        self.__project_base_dir = project_base_dir
        self.__logger = logger
        self.__target_paths_resolver = target_paths_resolver
        self.__package_metadata_loader = package_metadata_loader
        self.__current_and_release_deployer = current_and_release_deployer
        self.__package_deployer = package_deployer
        self.__cluster_restarter = cluster_restarter
        self.__jobs_deleter = jobs_deleter
        self.__jobs_creator_and_runner = jobs_creator_and_runner
        self.__notebooks_locator = notebooks_locator

    async def release(self, cluster_id: str):
        package_metadata = self.__package_metadata_loader.load(self.__project_base_dir)

        loop = asyncio.get_event_loop()

        package_release_future = loop.run_in_executor(None, self.__package_deployer.release, package_metadata)
        dbc_deploy_future = loop.run_in_executor(None, self.__current_and_release_deployer.release, package_metadata)

        await package_release_future
        await dbc_deploy_future

        self.__logger.info("--")

        consumer_notebooks = self.__notebooks_locator.locate_consumers()

        if consumer_notebooks:
            self.__cluster_restarter.restart(cluster_id)

            def create_job_notebook_path(consumer_notebook: Notebook):
                return str(
                    self.__target_paths_resolver.get_workspace_release_path(package_metadata) / consumer_notebook.databricks_relative_path
                )

            consumer_notebooks_release_paths = set(map(create_job_notebook_path, consumer_notebooks))

            self.__jobs_deleter.remove(consumer_notebooks_release_paths)

            self.__logger.info("--")

            self.__jobs_creator_and_runner.create_and_run(consumer_notebooks, cluster_id, package_metadata)

        self.__logger.info("Deployment completed")
