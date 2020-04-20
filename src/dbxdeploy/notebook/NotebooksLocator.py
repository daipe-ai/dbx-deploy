from pathlib import Path, PurePosixPath
from typing import List
from dbxdeploy.notebook.Notebook import Notebook
from dbxdeploy.notebook.RelativePathResolver import RelativePathResolver

class NotebooksLocator:

    def __init__(
        self,
        projectBaseDir: Path,
        pathsPatterns: list,
        consumerPathsPatterns: list,
        relativePathResolver: RelativePathResolver,
    ):
        self.__projectBaseDir = projectBaseDir
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

        basePath = self.__projectBaseDir.joinpath('src')  # type: Path

        filesGrabbed = []

        for pathPattern in pathsPatterns:
            filesGrabbed.extend(basePath.glob(pathPattern))

        return list(map(createNotebook, filesGrabbed)) # pylint: disable = cell-var-from-loop
