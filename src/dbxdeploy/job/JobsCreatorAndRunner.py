from typing import List
from databricks_api.databricks import DatabricksAPI
from dbxdeploy.job.JobCreator import JobCreator
from dbxdeploy.notebook.Notebook import Notebook
from dbxdeploy.package.PackageMetadata import PackageMetadata
from logging import Logger


class JobsCreatorAndRunner:
    def __init__(
        self,
        logger: Logger,
        dbx_api: DatabricksAPI,
        job_creator: JobCreator,
    ):
        self.__logger = logger
        self.__dbx_api = dbx_api
        self.__job_creator = job_creator

    def create_and_run(self, notebooks: List[Notebook], package_metadata: PackageMetadata):
        created_jobs = list(map(lambda notebook: self.__job_creator.create(notebook.databricks_relative_path, package_metadata), notebooks))

        self.__logger.info("--")

        for created_job in created_jobs:
            job_id = created_job["job_id"]
            notebook_release_path = created_job["notebook_release_path"]

            self.__logger.info("Running job #{}: {}".format(job_id, notebook_release_path))
            self.__dbx_api.jobs.run_now(job_id)

        self.__logger.info("--")
