from pathlib import PurePosixPath
from dbxdeploy.package.PackageMetadata import PackageMetadata
from databricks_api import DatabricksAPI
from logging import Logger
from dbxdeploy.deploy.TargetPathsResolver import TargetPathsResolver

class JobCreator:

    def __init__(
        self,
        clusterId: str,
        logger: Logger,
        dbxApi: DatabricksAPI,
        targetPathsResolver: TargetPathsResolver,
    ):
        self.__clusterId = clusterId
        self.__logger = logger
        self.__dbxApi = dbxApi
        self.__targetPathsResolver = targetPathsResolver

    def create(self, notebookPath: PurePosixPath, packageMetadata: PackageMetadata):
        notebookReleasePath = self.__targetPathsResolver.getWorkspaceReleasePath(packageMetadata) / notebookPath

        self.__logger.info('Creating job for {}'.format(str(notebookReleasePath)))

        job = self.__dbxApi.jobs.create_job(
            name=str(notebookPath),
            existing_cluster_id=self.__clusterId,
            max_retries=-1,
            min_retry_interval_millis=30*1000,
            retry_on_timeout=True,
            notebook_task=dict(
                notebook_path=str(notebookReleasePath)
            ),
            max_concurrent_runs=1
        )

        self.__logger.info('job #{} created'.format(job['job_id']))

        job['notebook_release_path'] = notebookReleasePath

        return job
