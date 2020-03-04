from pathlib import Path, PurePosixPath

class Notebook:

    def __init__(
        self,
        path: Path,
        relativePath: Path,
        databricksRelativePath: PurePosixPath,
        converterClass: str,
    ):
        self.__path = path
        self.__relativePath = relativePath
        self.__databricksRelativePath = databricksRelativePath
        self.__converterClass = converterClass

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def relativePath(self) -> Path:
        return self.__relativePath

    @property
    def databricksRelativePath(self) -> PurePosixPath:
        return self.__databricksRelativePath

    @property
    def converterClass(self) -> str:
        return self.__converterClass
