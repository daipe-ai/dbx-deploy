from typing import Iterable
from pathlib import Path
from dbxdeploy.package.PackageMetadata import PackageMetadata
from dbxdeploy.package.Dependency import Dependency


class LocalPathsResolver:
    def __init__(
        self,
        project_base_dir: Path,
    ):
        self.__project_base_dir = project_base_dir

    def get_package_dist_path(self, package_metadata: PackageMetadata):
        dist_dir = self.__project_base_dir.joinpath("dist")

        return dist_dir.joinpath(package_metadata.get_package_filename())

    def get_dependency_dist_path(self, dependency: Dependency):
        dist_dir = self.__project_base_dir.joinpath("dist")

        return self.get_dependency_path_from_dir(dist_dir, dependency)

    def get_dependency_path_from_dir(self, directory: Path, dependency: Dependency):
        dependency_paths = self.__get_all_dependency_paths_from_dir(directory)
        dependency_path = self.__find_dependency_path(dependency_paths, dependency)

        if dependency_path:
            return dependency_path

        raise Exception(f"Dependency {dependency.dependency_name}=={dependency.dependency_version} not found in {directory} directory")

    def get_linux_dependency_path_from_dir(self, directory: Path, dependency: Dependency):
        dependency_paths = self.__get_linux_dependency_paths_from_dir(directory)
        dependency_path = self.__find_dependency_path(dependency_paths, dependency)

        if dependency_path:
            return dependency_path

        raise Exception(
            f"Linux Dependency {dependency.dependency_name}=={dependency.dependency_version} not found in {directory} directory"
        )

    def get_dependency_filename_from_path(self, dependency_path: Path):
        return dependency_path.name

    def __get_dependency_name_from_path(self, dependency_path: Path):
        return dependency_path.stem.split("-")[0].replace("_", "-")

    def __get_dependency_version_from_path(self, dependency_path: Path):
        return dependency_path.stem.split("-")[1]

    def __get_dependency_platform_from_path(self, dependency_path: Path):
        return dependency_path.stem.split("-")[-1]

    def __get_all_dependency_paths_from_dir(self, directory: Path):
        return directory.glob("*.whl")

    def __get_linux_dependency_paths_from_dir(self, directory: Path):
        return [dependency_path for dependency_path in directory.glob("*.whl") if self.__is_linux_dependency(dependency_path)]

    def __is_linux_dependency(self, dependency_path: Path):
        platform = self.__get_dependency_platform_from_path(dependency_path).lower()

        return platform == "any" or "linux" in platform

    def __find_dependency_path(self, dependency_paths: Iterable[Path], dependency: Dependency):
        for dependency_path in dependency_paths:
            wheel_name = self.__get_dependency_name_from_path(dependency_path)
            wheel_version = self.__get_dependency_version_from_path(dependency_path)

            if wheel_name.lower() == dependency.dependency_name.lower() and wheel_version == dependency.dependency_version:
                return dependency_path

        return None
