import time
import re
from pathlib import Path
from pathlib import PurePosixPath
from logging import Logger
from databricks_api import DatabricksAPI
from dbxdeploy.package.PackageMetadata import PackageMetadata
from dbxdeploy.package.RequirementsCreator import RequirementsCreator
from dbxdeploy.dbfs.DbfsFileUploader import DbfsFileUploader
from dbxdeploy.dbfs.DbfsFileDownloader import DbfsFileDownloader
from dbxdeploy.package.requirements_regex import (
    CLASSIC_LINE_REGEX,
    GIT_LINE_REGEX,
    GIT_OLD_LINE1_REGEX,
    GIT_OLD_LINE2_REGEX,
)


class DependencyBuilder:
    def __init__(
        self,
        project_base_dir: Path,
        logger: Logger,
        dbx_api: DatabricksAPI,
        dbfs_file_uploader: DbfsFileUploader,
        dbfs_file_downloader: DbfsFileDownloader,
        job_cluster_definition: dict,
        requirements_creator: RequirementsCreator,
    ):
        self.__project_base_dir = project_base_dir
        self.__logger = logger
        self.__dbx_api = dbx_api
        self.__dbfs_file_uploader = dbfs_file_uploader
        self.__dbfs_file_downloader = dbfs_file_downloader
        self.__job_cluster_definition = job_cluster_definition
        self.__requirements_creator = requirements_creator

    def build(self, base_path: Path, package_metadata: PackageMetadata, dev_dependencies: bool = False):
        self.__logger.info("Preparing packages build script...")

        dbfs_build_dir = PurePosixPath(f"dbfs:/tmp/DependencyBuild/{package_metadata.get_job_run_name()}")
        dbfs_script_path = dbfs_build_dir.joinpath("download_dependencies.py")
        dbfs_dependencies_dir = dbfs_build_dir.joinpath("dependencies")
        local_dependencies_dir = base_path.joinpath("dependencies")
        unix_dependencies_dir = "/dbfs/" + dbfs_dependencies_dir.as_posix().lstrip("dbfs:/")
        requirements = self.__requirements_creator.export_to_string(base_path, dev_dependencies=dev_dependencies).splitlines()
        requirements = [
            requirement
            for requirement in requirements
            if re.match(CLASSIC_LINE_REGEX, requirement)
            or re.match(GIT_LINE_REGEX, requirement)
            or re.match(GIT_OLD_LINE1_REGEX, requirement)
            or re.match(GIT_OLD_LINE2_REGEX, requirement)
        ]

        script = (
            f"import sys, subprocess\n"
            f"requirements = {requirements}\n"
            f'subprocess.run([sys.executable, "-m", "pip", "wheel", "-w", "{unix_dependencies_dir}", *requirements], capture_output=False, encoding="utf-8")\n'
        ).encode("utf-8")

        self.__logger.info("Uploading build script to dbfs...")
        self.__dbfs_file_uploader.upload(script, str(dbfs_script_path))
        self.__logger.info("Build Script uploaded")

        self.__logger.info("Building python packages on Databricks cluster...")
        self.__submit_python_script_on_job_cluster(dbfs_script_path, package_metadata, wait=True)
        self.__logger.info("Build done")

        self.__logger.info(f"Downloading built packages to {local_dependencies_dir}...")
        self.__dbfs_file_downloader.download_directory(dbfs_dependencies_dir, local_dependencies_dir, overwrite=True)
        self.__logger.info("Download done, set dbxdeploy.target.package.offline_install: True in config and deploy")

    def __submit_python_script_on_job_cluster(
        self,
        script_path: PurePosixPath,
        package_metadata: PackageMetadata,
        wait: bool = False,
    ):
        submited_run = self.__dbx_api.jobs.submit_run(
            run_name=package_metadata.get_job_run_name(),
            new_cluster=self.__job_cluster_definition,
            spark_python_task=dict(python_file=str(script_path)),
        )

        run = self.__dbx_api.jobs.get_run(run_id=submited_run["run_id"])

        if wait:
            while run["state"]["life_cycle_state"] not in ["TERMINATED", "SKIPPED", "INTERNAL_ERROR"]:
                time.sleep(15)
                run = self.__dbx_api.jobs.get_run(run_id=submited_run["run_id"])

            return self.__dbx_api.jobs.get_run_output(submited_run["run_id"])

        return run
