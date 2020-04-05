from pathlib import Path
from typing import List
from dbxdeploy.notebook.ConverterResolver import ConverterResolver
from dbxdeploy.notebook.Notebook import Notebook

class NotebooksLocator:

    def __init__(
        self,
        projectBasePath: Path,
        converterResolver: ConverterResolver,
    ):
        self.__projectBasePath = projectBasePath
        self.__converterResolver = converterResolver

    def locate(self) -> List[Notebook]:
        convertersWithGlobPatterns = self.__converterResolver.getGlobPatterns()

        return self.__locate(convertersWithGlobPatterns)

    def locateConsumers(self):
        convertersWithGlobPatterns = self.__converterResolver.getConsumerGlobPatterns()

        return self.__locate(convertersWithGlobPatterns)

    def __locate(self, globPatternsByConverter: List[List[str]]):
        basePath = self.__projectBasePath.joinpath('src')  # type: Path
        output = []

        def createNotebook(path: Path):
            return Notebook(
                path,
                path.relative_to(self.__projectBasePath),
                path.relative_to(self.__projectBasePath).relative_to('src').with_suffix('').as_posix(),
            )

        for globPatterns in globPatternsByConverter:
            filesGrabbed = []

            for globPattern in globPatterns:
                filesGrabbed.extend(basePath.glob(globPattern))

                output += list(map(createNotebook, filesGrabbed)) # pylint: disable = cell-var-from-loop

        return output
