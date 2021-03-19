from databricks_api import DatabricksAPI
from pathlib import PurePosixPath
from dbxdeploy.package.PackageMetadata import PackageMetadata
import re


class RunsGetter:
    def __init__(self, cluster_id: str, workspace_base_dir: PurePosixPath, dbx_api: DatabricksAPI):
        self.__cluster_id = cluster_id
        self.__workspace_base_dir = workspace_base_dir
        self.__dbx_api = dbx_api

    def get(self, notebook_path: PurePosixPath, package_metadata: PackageMetadata):
        notebook_runs = []

        page = 1
        limit = 50

        while True:
            response = self.__dbx_api.jobs.list_runs(active_only=True, limit=limit, offset=((page - 1) * limit))

            if "runs" in response:
                new_runs = list(filter(lambda run: self.__filter_run(run, notebook_path, package_metadata), response["runs"]))
                notebook_runs = notebook_runs + new_runs

            if response["has_more"] is False:
                break

            page += 1

        return notebook_runs

    def __filter_run(self, run: dict, notebook_path: PurePosixPath, package_metadata: PackageMetadata):
        reg_ex = package_metadata.get_notebook_path_reg_ex(self.__workspace_base_dir, notebook_path)

        if "notebook_task" not in run["task"]:
            return False

        return (
            re.match(reg_ex, run["task"]["notebook_task"]["notebook_path"])
            and run["cluster_spec"]["existing_cluster_id"] == self.__cluster_id
        )
