from pathlib import PurePosixPath
from dbxdeploy.job.RunsGetter import RunsGetter
from dbxdeploy.package.PackageMetadata import PackageMetadata
from databricks_api import DatabricksAPI
from logging import Logger

class NotebookKiller:

    def __init__(
        self,
        logger: Logger,
        dbxApi: DatabricksAPI,
        runsGetter: RunsGetter,
    ):
        self.__logger = logger
        self.__dbxApi = dbxApi
        self.__runsGetter = runsGetter

    def killIfRunning(self, notebookPath: PurePosixPath, packageMetadata: PackageMetadata):
        self.__logger.info('Looking for jobs running the {} notebook'.format(notebookPath))
        previousNotebookRuns = self.__runsGetter.get(notebookPath, packageMetadata)

        if previousNotebookRuns:
            for runningJob in previousNotebookRuns:
                self.__logger.warning('Killing JOB #{} for {}'.format(str(runningJob['run_id']), runningJob['task']['notebook_task']['notebook_path']))
                self.__dbxApi.jobs.cancel_run(runningJob['run_id'])
        else:
            self.__logger.info('notebook {} is not running in any job'.format(notebookPath))
