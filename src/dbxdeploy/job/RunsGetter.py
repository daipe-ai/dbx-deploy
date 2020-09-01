from databricks_api import DatabricksAPI
from pathlib import PurePosixPath
from dbxdeploy.package.PackageMetadata import PackageMetadata
import re

class RunsGetter:

    def __init__(
        self,
        clusterId: str,
        workspaceBaseDir: PurePosixPath,
        dbxApi: DatabricksAPI
    ):
        self.__clusterId = clusterId
        self.__workspaceBaseDir = workspaceBaseDir
        self.__dbxApi = dbxApi

    def get(self, notebookPath: PurePosixPath, packageMetadata: PackageMetadata):
        notebookRuns = []

        page = 1
        limit = 50

        while True:
            response = self.__dbxApi.jobs.list_runs(
                active_only=True,
                limit=limit,
                offset=((page - 1) * limit)
            )

            if 'runs' in response:
                newRuns = list(filter(lambda run: self.__filterRun(run, notebookPath, packageMetadata), response['runs']))
                notebookRuns = notebookRuns + newRuns

            if response['has_more'] is False:
                break

            page += 1

        return notebookRuns

    def __filterRun(self, run: dict, notebookPath: PurePosixPath, packageMetadata: PackageMetadata):
        regEx = packageMetadata.getNotebookPathRegEx(self.__workspaceBaseDir, notebookPath)

        if 'notebook_task' not in run['task']:
            return False

        return (
            re.match(regEx, run['task']['notebook_task']['notebook_path'])
            and run['cluster_spec']['existing_cluster_id'] == self.__clusterId
        )
