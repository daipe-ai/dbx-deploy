from pathlib import PurePosixPath

class RelativePathResolver:

    def __init__(
        self,
        baseDirPath: str,
    ):
        self.__baseDirPath = baseDirPath

    def resolve(self, notebookPath: PurePosixPath):
        return notebookPath.relative_to(self.__baseDirPath).with_suffix('')
