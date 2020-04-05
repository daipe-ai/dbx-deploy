from pathlib import Path
from typing import List
from dbxdeploy.notebook.Notebook import Notebook

class NotebooksLocator:

    def __init__(
        self,
        projectBasePath: Path,
        pathsPatterns: list,
        consumerPathsPatterns: list,
    ):
        self.__projectBasePath = projectBasePath
        self.__pathsPatterns = pathsPatterns
        self.__consumerPathsPatterns = consumerPathsPatterns

    def locate(self) -> List[Notebook]:
        return self.__locate(self.__pathsPatterns)

    def locateConsumers(self):
        return self.__locate(self.__consumerPathsPatterns)

    def __locate(self, pathsPatterns: list):
        def createNotebook(path: Path):
            return Notebook(
                path,
                path.relative_to(self.__projectBasePath),
                path.relative_to(self.__projectBasePath).relative_to('src').with_suffix('').as_posix(),
            )

        basePath = self.__projectBasePath.joinpath('src')  # type: Path

        filesGrabbed = []

        for pathPattern in pathsPatterns:
            filesGrabbed.extend(basePath.glob(pathPattern))

        return list(map(createNotebook, filesGrabbed)) # pylint: disable = cell-var-from-loop
