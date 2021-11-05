from pathlib import Path, PurePosixPath
from typing import List
from dbxdeploy.notebook.Notebook import Notebook
from dbxdeploy.notebook.RelativePathResolver import RelativePathResolver


class NotebooksLocator:
    def __init__(
        self,
        project_base_dir: Path,
        relative_base_dir: str,
        paths_patterns: list,
        consumer_paths_patterns: list,
        master_package_notebook_path: str,
        bootstrap_notebook_path: str,
        relative_path_resolver: RelativePathResolver,
    ):
        self.__project_base_dir = project_base_dir
        self.__relative_base_dir = relative_base_dir
        self.__paths_patterns = paths_patterns
        self.__consumer_paths_patterns = consumer_paths_patterns
        self.__master_package_notebook_path = master_package_notebook_path
        self.__bootstrap_notebook_path = bootstrap_notebook_path
        self.__relative_path_resolver = relative_path_resolver

    def locate(self) -> List[Notebook]:
        return self.__locate(self.__paths_patterns)

    def locate_consumers(self):
        return self.__locate(self.__consumer_paths_patterns)

    def bootstrap_notebook_present(self) -> bool:
        return self.__project_base_dir.joinpath(self.__bootstrap_notebook_path).is_file()

    def master_package_notebook_present(self) -> bool:
        return self.__project_base_dir.joinpath(self.__master_package_notebook_path).is_file()

    def locate_bootstrap_notebook(self) -> Notebook:
        notebook_path = self.__project_base_dir.joinpath(self.__bootstrap_notebook_path)
        pure_posix_path = PurePosixPath(notebook_path.relative_to(self.__project_base_dir).as_posix())

        return Notebook(
            notebook_path, notebook_path.relative_to(self.__project_base_dir), self.__relative_path_resolver.resolve(pure_posix_path)
        )

    def locate_master_package_notebook(self) -> Notebook:
        notebook_path = self.__project_base_dir.joinpath(self.__master_package_notebook_path)
        pure_posix_path = PurePosixPath(notebook_path.relative_to(self.__project_base_dir).as_posix())

        return Notebook(
            notebook_path, notebook_path.relative_to(self.__project_base_dir), self.__relative_path_resolver.resolve(pure_posix_path)
        )

    def check_at_least_one_bootstrap_ntb_present(self):
        if not self.bootstrap_notebook_present() and not self.master_package_notebook_present():
            raise Exception(
                f"Neither bootstrap nor install_master_package notebook could be found at "
                f"'{self.__bootstrap_notebook_path}', '{self.__master_package_notebook_path}'"
            )

    def __locate(self, paths_patterns: list):
        def create_notebook(path: Path):
            pure_posix_path = PurePosixPath(path.relative_to(self.__project_base_dir).as_posix())
            return Notebook(path, path.relative_to(self.__project_base_dir), self.__relative_path_resolver.resolve(pure_posix_path))

        base_dir = self.__project_base_dir.joinpath(self.__relative_base_dir)

        files_grabbed = []

        for path_pattern in paths_patterns:
            cleaned = [file for file in base_dir.glob(path_pattern) if not PurePosixPath(file).match(".ipynb_checkpoints/*.py")]
            files_grabbed.extend(cleaned)

        return list(map(create_notebook, files_grabbed))
