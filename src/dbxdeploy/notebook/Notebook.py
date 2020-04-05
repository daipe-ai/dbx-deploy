from pathlib import Path, PurePosixPath

class Notebook:

    def __init__(
        self,
        path: Path,
        relativePath: Path,
        databricksRelativePath: PurePosixPath,
    ):
        self.__path = path
        self.__relativePath = relativePath
        self.__databricksRelativePath = databricksRelativePath

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def relativePath(self) -> Path:
        return self.__relativePath

    @property
    def databricksRelativePath(self) -> PurePosixPath:
        return self.__databricksRelativePath
