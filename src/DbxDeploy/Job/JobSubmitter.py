import subprocess
from box import Box
from databricks_api import DatabricksAPI
from DbxDeploy.Setup.Version.VersionInterface import VersionInterface
from pathlib import PurePosixPath

class JobSubmitter:

    def __init__(
        self,
        clusterId: str,
        dbxProjectRoot: str,
        browserConfig: Box,
        dbxApi: DatabricksAPI
    ):
        self.__clusterId = clusterId
        self.__dbxProjectRoot = dbxProjectRoot
        self.__browserConfig = browserConfig
        self.__dbxApi = dbxApi

    def submit(self, notebookPath: PurePosixPath, version: VersionInterface):
        notebookReleasePath = version.getDbxVersionPath(self.__dbxProjectRoot) + '/' + str(notebookPath)

        print('Submitting job for {}'.format(notebookPath))

        submitedRun = self.__dbxApi.jobs.submit_run(
            run_name=version.getTimeAndRandomString(),
            existing_cluster_id=self.__clusterId,
            notebook_task=dict(
                notebook_path=notebookReleasePath
            )
        )

        print('Job created with ID: {}'.format(str(submitedRun['run_id'])))

        run = self.__dbxApi.jobs.get_run(
            run_id=submitedRun['run_id']
        )

        self.__openJobInDatabricks(run['run_page_url'])

    def __openJobInDatabricks(self, runUrl: str):
        print('Opening {}'.format(runUrl))

        arguments = [self.__browserConfig.path]

        for argument in self.__browserConfig.arguments:
            arguments.append(argument.replace('{runUrl}', runUrl))

        subprocess.run(arguments)
