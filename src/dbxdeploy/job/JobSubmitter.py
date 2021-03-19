import subprocess
from box import Box
from databricks_api import DatabricksAPI
from dbxdeploy.package.PackageMetadata import PackageMetadata
from pathlib import PurePosixPath
from logging import Logger


class JobSubmitter:
    def __init__(
        self,
        cluster_id: str,
        workspace_base_dir: PurePosixPath,
        browser_config: Box,
        logger: Logger,
        dbx_api: DatabricksAPI,
    ):
        self.__cluster_id = cluster_id
        self.__workspace_base_dir = workspace_base_dir
        self.__browser_config = browser_config
        self.__logger = logger
        self.__dbx_api = dbx_api

    def submit(self, notebook_path: PurePosixPath, package_metadata: PackageMetadata):
        notebook_release_path = self.__workspace_base_dir.joinpath(notebook_path)

        self.__logger.info(f"Submitting job for {notebook_release_path} to cluster {self.__cluster_id}")

        submited_run = self.__dbx_api.jobs.submit_run(
            run_name=package_metadata.get_job_run_name(),
            existing_cluster_id=self.__cluster_id,
            notebook_task=dict(notebook_path=str(notebook_release_path)),
        )

        self.__logger.info(f'Job {str(submited_run["run_id"])} created')

        run = self.__dbx_api.jobs.get_run(run_id=submited_run["run_id"])

        self.__open_job_in_databricks(run["run_page_url"])

    def __open_job_in_databricks(self, run_url: str):
        self.__logger.info(f"Opening {run_url}")

        arguments = [self.__browser_config.path]

        for argument in self.__browser_config.arguments:
            arguments.append(argument.replace("{run_url}", run_url))

        subprocess.run(arguments, check=True)
