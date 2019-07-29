from pathlib import PurePosixPath
from DbxDeploy.Job.RunsGetter import RunsGetter
from DbxDeploy.Setup.Version.VersionInterface import VersionInterface
from databricks_api import DatabricksAPI

class NotebookKiller:

    def __init__(
        self,
        runsGetter: RunsGetter,
        dbxApi: DatabricksAPI
    ):
        self.__runsGetter = runsGetter
        self.__dbxApi = dbxApi

    def killIfRunning(self, notebookPath: PurePosixPath, version: VersionInterface):
        previousNotebookRuns = self.__runsGetter.get(notebookPath, version)

        for runningJob in previousNotebookRuns:
            print('Killing JOB #{} for {}'.format(str(runningJob['run_id']), runningJob['task']['notebook_task']['notebook_path']))
            self.__dbxApi.jobs.cancel_run(runningJob['run_id'])
