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
        relative_path_resolver: RelativePathResolver,
    ):
        self.__project_base_dir = project_base_dir
        self.__relative_base_dir = relative_base_dir
        self.__paths_patterns = paths_patterns
        self.__consumer_paths_patterns = consumer_paths_patterns
        self.__master_package_notebook_path = master_package_notebook_path
        self.__relative_path_resolver = relative_path_resolver

    def locate(self) -> List[Notebook]:
        return self.__locate(self.__paths_patterns)

    def locate_consumers(self):
        return self.__locate(self.__consumer_paths_patterns)

    def locate_master_package_notebook(self) -> Notebook:
        notebook_path = self.__project_base_dir.joinpath(self.__master_package_notebook_path)
        pure_posix_path = PurePosixPath(notebook_path.relative_to(self.__project_base_dir).as_posix())

        if not notebook_path.is_file():
            raise Exception(f"Notebook at {notebook_path} not found")

        return Notebook(
            notebook_path, notebook_path.relative_to(self.__project_base_dir), self.__relative_path_resolver.resolve(pure_posix_path)
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
