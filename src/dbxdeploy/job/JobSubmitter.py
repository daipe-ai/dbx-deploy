import subprocess
from box import Box
from databricks_api import DatabricksAPI
from dbxdeploy.package.PackageMetadata import PackageMetadata
from pathlib import PurePosixPath
from logging import Logger

class JobSubmitter:

    def __init__(
        self,
        clusterId: str,
        dbxProjectRoot: PurePosixPath,
        browserConfig: Box,
        logger: Logger,
        dbxApi: DatabricksAPI,
    ):
        self.__clusterId = clusterId
        self.__dbxProjectRoot = dbxProjectRoot
        self.__browserConfig = browserConfig
        self.__logger = logger
        self.__dbxApi = dbxApi

    def submit(self, notebookPath: PurePosixPath, packageMetadata: PackageMetadata):
        notebookReleasePath = self.__dbxProjectRoot.joinpath(notebookPath)

        self.__logger.info('Submitting job for {} to cluster {}'.format(notebookReleasePath, self.__clusterId))

        submitedRun = self.__dbxApi.jobs.submit_run(
            run_name=packageMetadata.getJobRunName(),
            existing_cluster_id=self.__clusterId,
            notebook_task=dict(
                notebook_path=str(notebookReleasePath)
            )
        )

        self.__logger.info('job {} created'.format(str(submitedRun['run_id'])))

        run = self.__dbxApi.jobs.get_run(
            run_id=submitedRun['run_id']
        )

        self.__openJobInDatabricks(run['run_page_url'])

    def __openJobInDatabricks(self, runUrl: str):
        self.__logger.info('Opening {}'.format(runUrl))

        arguments = [self.__browserConfig.path]

        for argument in self.__browserConfig.arguments:
            arguments.append(argument.replace('{runUrl}', runUrl))

        subprocess.run(arguments, check=True)
