from pathlib import PurePosixPath
from typing import List
from dbxdeploy.notebook.converter.ConverterGlobPatterns import ConverterGlobPatterns
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface

class ConverterResolver:

    def __init__(
        self,
        converters: List[NotebookConverterInterface]
    ):
        self.__converters = converters

    def isSupported(self, path: PurePosixPath):
        fileExtension = path.suffix[1:]

        for converter in self.__converters:
            if converter.resolves(fileExtension) is True:
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
