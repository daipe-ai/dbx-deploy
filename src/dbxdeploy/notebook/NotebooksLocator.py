from pathlib import Path
from typing import List
from dbxdeploy.notebook.ConverterResolver import ConverterResolver
from dbxdeploy.notebook.Notebook import Notebook
from dbxdeploy.notebook.converter.ConverterGlobPatterns import ConverterGlobPatterns

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

    def __locate(self, convertersWithGlobPatterns: List[ConverterGlobPatterns]):
        basePath = self.__projectBasePath.joinpath('src')  # type: Path
        output = []

        def createNotebook(path: Path, converterClass: str):
            return Notebook(
                path,
                path.relative_to(self.__projectBasePath),
                path.relative_to(self.__projectBasePath).relative_to('src').with_suffix('').as_posix(),
                converterClass,
            )

        for converterGlobPatterns in convertersWithGlobPatterns:
            filesGrabbed = []

            for globPattern in converterGlobPatterns.globPatterns:
                filesGrabbed.extend(basePath.glob(globPattern))

                output += list(map(lambda fileGrabbed: createNotebook(fileGrabbed, converterGlobPatterns.converterClass), filesGrabbed)) # pylint: disable = cell-var-from-loop

        return output
