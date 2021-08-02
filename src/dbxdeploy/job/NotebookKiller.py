from pathlib import PurePosixPath
from dbxdeploy.job.RunsGetter import RunsGetter
from dbxdeploy.package.PackageMetadata import PackageMetadata
from databricks_api import DatabricksAPI
from logging import Logger


class NotebookKiller:
    def __init__(
        self,
        logger: Logger,
        dbx_api: DatabricksAPI,
        runs_getter: RunsGetter,
    ):
        self.__logger = logger
        self.__dbx_api = dbx_api
        self.__runs_getter = runs_getter

    def kill_if_running(self, notebook_path: PurePosixPath, cluster_id: str, package_metadata: PackageMetadata):
        self.__logger.info("Looking for jobs running the {} notebook".format(notebook_path))
        previous_notebook_runs = self.__runs_getter.get(notebook_path, cluster_id, package_metadata)

        if previous_notebook_runs:
            for running_job in previous_notebook_runs:
                self.__logger.warning(
                    "Killing JOB #{} for {}".format(str(running_job["run_id"]), running_job["task"]["notebook_task"]["notebook_path"])
                )
                self.__dbx_api.jobs.cancel_run(running_job["run_id"])
        else:
            self.__logger.info("notebook {} is not running in any job".format(notebook_path))
