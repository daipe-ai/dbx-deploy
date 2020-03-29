from pathlib import PurePosixPath
from typing import List
from dbxdeploy.notebook.converter.ConverterGlobPatterns import ConverterGlobPatterns
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException

class ConverterResolver:

    def __init__(
        self,
        converters: List[NotebookConverterInterface]
    ):
        self.__converters = converters

    def isSupported(self, path: PurePosixPath) -> bool:
        fileExtension = path.suffix[1:]

        for converter in self.__converters:
            if fileExtension not in converter.getSupportedExtensions():
                continue

            try:
                converter.loadSource(fileExtension)
            except UnexpectedSourceException:
                continue

            return True

        return False

    def getSupportedFormatsDescriptions(self) -> list:
        return list(map(lambda converter: converter.getDescription(), self.__converters))

    def resolve(self, converterClass: str) -> NotebookConverterInterface:
        for converter in self.__converters:
            if converter.__class__.__name__ == converterClass:
                return converter

        raise Exception('No converter for: {}'.format(converterClass))

    def getGlobPatterns(self):
        patterns = []

        for converter in self.__converters:
            className = converter.__class__.__name__

            patterns.append(ConverterGlobPatterns(className, converter.getGlobPatterns()))

        return patterns

    def getConsumerGlobPatterns(self):
        patterns = []

        for converter in self.__converters:
            className = converter.__class__.__name__

            patterns.append(ConverterGlobPatterns(className, converter.getConsumerGlobPatterns()))

        return patterns
