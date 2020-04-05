from pathlib import Path
from typing import List
from dbxdeploy.notebook.ConverterNotFoundException import ConverterNotFoundException
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException

class ConverterResolver:

    def __init__(
        self,
        converters: List[NotebookConverterInterface]
    ):
        self.__converters = converters

    def getSupportedFormatsDescriptions(self) -> list:
        return list(map(lambda converter: converter.getDescription(), self.__converters))

    def resolve(self, path: Path, content):
        fileExtension = path.suffix[1:]

        for converter in self.__converters:
            if fileExtension not in converter.getSupportedExtensions():
                continue

            try:
                converter.validateSource(content)
            except UnexpectedSourceException:
                continue

            return converter

        raise ConverterNotFoundException()

    def isSupported(self, path: Path, content) -> bool:
        try:
            self.resolve(path, content)

            return True
        except ConverterNotFoundException:
            return False

    def getGlobPatterns(self):
        return list(map(lambda converter: converter.getGlobPatterns(), self.__converters))

    def getConsumerGlobPatterns(self):
        return list(map(lambda converter: converter.getConsumerGlobPatterns(), self.__converters))
