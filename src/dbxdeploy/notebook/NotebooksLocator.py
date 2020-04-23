from pathlib import Path, PurePosixPath
from typing import List
from dbxdeploy.notebook.Notebook import Notebook
from dbxdeploy.notebook.RelativePathResolver import RelativePathResolver

class NotebooksLocator:

    def __init__(
        self,
        projectBaseDir: Path,
        relativeBaseDir: str,
        pathsPatterns: list,
        consumerPathsPatterns: list,
        relativePathResolver: RelativePathResolver,
    ):
        self.__projectBaseDir = projectBaseDir
        self.__relativeBaseDir = relativeBaseDir
        self.__pathsPatterns = pathsPatterns
        self.__consumerPathsPatterns = consumerPathsPatterns
        self.__relativePathResolver = relativePathResolver

    def locate(self) -> List[Notebook]:
        return self.__locate(self.__pathsPatterns)

    def locateConsumers(self):
        return self.__locate(self.__consumerPathsPatterns)

    def __locate(self, pathsPatterns: list):
        def createNotebook(path: Path):
            purePosixPath = PurePosixPath(path.relative_to(self.__projectBaseDir).as_posix())

            return Notebook(
                path,
                path.relative_to(self.__projectBaseDir),
                self.__relativePathResolver.resolve(purePosixPath)
            )

        baseDir = self.__projectBaseDir.joinpath(self.__relativeBaseDir)

        filesGrabbed = []

        for pathPattern in pathsPatterns:
            filesGrabbed.extend(baseDir.glob(pathPattern))

        return list(map(createNotebook, filesGrabbed)) # pylint: disable = cell-var-from-loop
