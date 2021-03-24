from typing import List
from datetime import datetime
from pathlib import PurePosixPath
from dbxdeploy.package.Dependency import Dependency


class PackageMetadata:
    def __init__(
        self,
        package_name: str,
        package_version: str,
        date_time: datetime,
        random_string: str,
        dependencies: List[Dependency],
    ):
        self.__package_name = package_name
        self.__package_version = package_version
        self.__date_time = date_time
        self.__random_string = random_string
        self.__dependencies = dependencies

    @property
    def package_name(self):
        return self.__package_name

    @property
    def package_version(self):
        return self.__package_version

    @property
    def date_time(self):
        return self.__date_time

    @property
    def random_string(self):
        return self.__random_string

    @property
    def dependencies(self):
        return self.__dependencies

    def get_package_filename(self):
        return "{}-{}-py3-none-any.whl".format(self.__get_package_name(), self.__package_version)

    def get_notebook_path_reg_ex(self, workspace_base_dir: PurePosixPath, notebook_path: PurePosixPath) -> str:
        return "^" + str(workspace_base_dir) + "/([^/]+)/" + str(notebook_path) + "$"

    def get_job_run_name(self) -> str:
        return self.__date_time.strftime("%Y-%m-%d_%H-%M-%S") + "_" + self.__random_string

    def get_dependency_by_name(self, dependency_name: str) -> Dependency:
        for dependency in self.__dependencies:
            if dependency.dependency_name == dependency_name:
                return dependency

        raise Exception(f"Dependency {dependency_name} not found")

    def __get_package_name(self):
        return self.__package_name.replace("-", "_")
