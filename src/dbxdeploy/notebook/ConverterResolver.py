from pathlib import Path, PurePosixPath
from typing import List
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

    def resolve(self, path: Path) -> NotebookConverterInterface:
        fileExtension = path.suffix[1:]

        for converter in self.__converters:
            if converter.resolves(fileExtension) is True:
                return converter

        raise Exception('No converter for .{}'.format(fileExtension))

    def getGlobPatterns(self):
        patterns = []

        for converter in self.__converters:
            patterns = patterns + converter.getGlobPatterns()

        return patterns

    def getConsumerGlobPatterns(self):
        patterns = []

        for converter in self.__converters:
            patterns = patterns + converter.getConsumerGlobPatterns()

        return patterns
