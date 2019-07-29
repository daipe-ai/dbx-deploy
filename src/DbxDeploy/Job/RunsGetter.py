from databricks_api import DatabricksAPI
from pathlib import PurePosixPath
from DbxDeploy.Setup.Version.VersionInterface import VersionInterface
import re

class RunsGetter:

    def __init__(
        self,
        clusterId: str,
        dbxProjectRoot: str,
        dbxApi: DatabricksAPI
    ):
        self.__clusterId = clusterId
        self.__dbxProjectRoot = dbxProjectRoot
        self.__dbxApi = dbxApi

    def get(self, notebookPath: PurePosixPath, version: VersionInterface):
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
                newRuns = list(filter(lambda run: self.__filterRun(run, notebookPath, version), response['runs']))
                notebookRuns = notebookRuns + newRuns

            if response['has_more'] is False:
                break

            page += 1

        return notebookRuns

    def __filterRun(self, run: dict, notebookPath: PurePosixPath, version: VersionInterface):
        regEx = version.getDbxVersionPathRegEx(self.__dbxProjectRoot) + '/' + str(notebookPath) + '$'

        return (
            re.match(regEx, run['task']['notebook_task']['notebook_path'])
            and run['cluster_spec']['existing_cluster_id'] == self.__clusterId
        )
