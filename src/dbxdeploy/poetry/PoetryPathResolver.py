from pathlib import Path

class PoetryPathResolver:

    def __init__(
        self,
        poetryPath: str
    ):
        self.__poetryPath = poetryPath

    def getPoetryPath(self) -> Path:
        return Path(self.__poetryPath).expanduser()
