import sys
import shutil
from pathlib import Path
from dbxdeploy.package.BootstrapConfigAppender import BootstrapConfigAppender
from dbxdeploy.package.LockedPyprojectCreator import LockedPyprojectCreator
from dbxdeploy.package.PackageMetadata import PackageMetadata
from dbxdeploy.deploy.LocalPathsResolver import LocalPathsResolver
from dbxdeploy.poetry.PoetryPathResolver import PoetryPathResolver
from dbxdeploy.shell.runner import run_shell_command
from dbxdeploy.filesystem.utils import delete_directory_content_recursive


class PackageBuilder:
    def __init__(
        self,
        project_base_dir: Path,
        offline_install: bool,
        locked_pyproject_creator: LockedPyprojectCreator,
        bootstrap_config_appender: BootstrapConfigAppender,
        local_paths_resolver: LocalPathsResolver,
        poetry_path_resolver: PoetryPathResolver,
    ):
        self.__project_base_dir = project_base_dir
        self.__offline_install = offline_install
        self.__locked_pyproject_creator = locked_pyproject_creator
        self.__bootstrap_config_appender = bootstrap_config_appender
        self.__local_paths_resolver = local_paths_resolver
        self.__poetry_path_resolver = poetry_path_resolver

    def build(self, base_path: Path, package_metadata: PackageMetadata):
        dist_dir = base_path.joinpath("dist")

        delete_directory_content_recursive(dist_dir)

        pyproject_orig_path = base_path.joinpath("pyproject.toml")
        pyproject_new_path = base_path.joinpath("pyproject.toml.new")

        self.__locked_pyproject_creator.create(package_metadata, pyproject_orig_path, pyproject_new_path)

        package_file_name = package_metadata.get_package_filename()
        package_path = self.__project_base_dir.joinpath(Path("dist")).joinpath(package_file_name)

        self.__build_wheel(pyproject_orig_path, pyproject_new_path, base_path)

        self.__bootstrap_config_appender.append(package_path)

        if self.__offline_install:
            self.__build_wheelhouse(base_path, package_metadata)

    def __build_wheel(self, pyproject_orig_path: Path, pyproject_new_path: Path, base_path: Path):
        pyproject_dist = base_path.joinpath("dist/pyproject.toml")
        pyproject_bak_path = base_path.joinpath("pyproject.toml.bak")

        pyproject_orig_path.rename(pyproject_bak_path)
        pyproject_new_path.rename(pyproject_orig_path)

        python_executable = sys.executable
        poetry_path = self.__poetry_path_resolver.get_poetry_path()

        try:
            run_shell_command(f"{python_executable} {poetry_path} build --format wheel", cwd=str(base_path), shell=True)
        except BaseException:
            pass
        finally:
            pyproject_orig_path.replace(pyproject_dist)
            pyproject_bak_path.rename(pyproject_orig_path)

    def __build_wheelhouse(self, base_path: Path, package_metadata: PackageMetadata):
        dependencies_dir = base_path.joinpath("dependencies")
        dist_dir = base_path.joinpath("dist")

        if not dependencies_dir.is_dir():
            raise Exception(f"Cannot find dependencies dir at {dependencies_dir}")

        for dependency in package_metadata.dependencies:
            dependency_wheel = self.__local_paths_resolver.get_linux_dependency_path_from_dir(dependencies_dir, dependency)

            shutil.copy(dependency_wheel, dist_dir)
