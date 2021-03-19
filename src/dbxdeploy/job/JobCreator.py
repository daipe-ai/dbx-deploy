from pathlib import PurePosixPath
from dbxdeploy.package.PackageMetadata import PackageMetadata
from databricks_api import DatabricksAPI
from logging import Logger
from dbxdeploy.deploy.TargetPathsResolver import TargetPathsResolver


class JobCreator:
    def __init__(
        self,
        cluster_id: str,
        logger: Logger,
        dbx_api: DatabricksAPI,
        target_paths_resolver: TargetPathsResolver,
    ):
        self.__cluster_id = cluster_id
        self.__logger = logger
        self.__dbx_api = dbx_api
        self.__target_paths_resolver = target_paths_resolver

    def create(self, notebook_path: PurePosixPath, package_metadata: PackageMetadata):
        notebook_release_path = self.__target_paths_resolver.get_workspace_release_path(package_metadata) / notebook_path

        self.__logger.info("Creating job for {}".format(str(notebook_release_path)))

        job = self.__dbx_api.jobs.create_job(
            name=str(notebook_path),
            existing_cluster_id=self.__cluster_id,
            max_retries=-1,
            min_retry_interval_millis=30 * 1000,
            retry_on_timeout=True,
            notebook_task=dict(notebook_path=str(notebook_release_path)),
            max_concurrent_runs=1,
        )

        self.__logger.info("job #{} created".format(job["job_id"]))

        job["notebook_release_path"] = notebook_release_path

        return job
