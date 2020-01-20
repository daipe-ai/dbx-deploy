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
        patterns = self.__converterResolver.getGlobPatterns()

        return self.__locate(patterns)


    def locateConsumers(self):
        patterns = self.__converterResolver.getConsumerGlobPatterns()

        return self.__locate(patterns)

    def __locate(self, patterns: list):
        basePath = self.__projectBasePath.joinpath('src')  # type: Path

        filesGrabbed = []

        for pattern in patterns:
            filesGrabbed.extend(basePath.glob(pattern))

        def createNotebook(path: Path):
            return Notebook(
                path,
                path.relative_to(self.__projectBasePath),
                path.relative_to(self.__projectBasePath).relative_to('src').with_suffix('').as_posix()
            )

        return list(map(createNotebook, filesGrabbed))
