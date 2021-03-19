from pathlib import Path, PurePosixPath


class Notebook:
    def __init__(
        self,
        path: Path,
        relative_path: Path,
        databricks_relative_path: PurePosixPath,
    ):
        self.__path = path
        self.__relative_path = relative_path
        self.__databricks_relative_path = databricks_relative_path

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def relative_path(self) -> Path:
        return self.__relative_path

    @property
    def databricks_relative_path(self) -> PurePosixPath:
        return self.__databricks_relative_path
