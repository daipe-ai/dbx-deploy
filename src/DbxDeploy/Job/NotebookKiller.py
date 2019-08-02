from pathlib import PurePosixPath
from DbxDeploy.Job.RunsGetter import RunsGetter
from DbxDeploy.Setup.Version.VersionInterface import VersionInterface
from databricks_api import DatabricksAPI
from logging import Logger

class NotebookKiller:

    def __init__(
        self,
        logger: Logger,
        runsGetter: RunsGetter,
        dbxApi: DatabricksAPI
    ):
        self.__logger = logger
        self.__runsGetter = runsGetter
        self.__dbxApi = dbxApi

    def killIfRunning(self, notebookPath: PurePosixPath, version: VersionInterface):
        self.__logger.info('Looking for jobs running the {} notebook'.format(notebookPath))
        previousNotebookRuns = self.__runsGetter.get(notebookPath, version)

        if len(previousNotebookRuns) > 0:
            for runningJob in previousNotebookRuns:
                self.__logger.warning('Killing JOB #{} for {}'.format(str(runningJob['run_id']), runningJob['task']['notebook_task']['notebook_path']))
                self.__dbxApi.jobs.cancel_run(runningJob['run_id'])
        else:
            self.__logger.info('Notebook {} is not running in any job'.format(notebookPath))
