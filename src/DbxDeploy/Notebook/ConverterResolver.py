from pathlib import Path
from typing import List
from DbxDeploy.Notebook.Converter.NotebookConverterInterface import NotebookConverterInterface

class ConverterResolver:

    def __init__(
        self,
        converters: List[NotebookConverterInterface]
    ):
        self.__converters = converters

    def resolve(self, path: Path) -> NotebookConverterInterface:
        fileExtension = path.suffix[1:]

        for converter in self.__converters:
            if converter.resolves(fileExtension) is True:
                return converter

        raise Exception('No converter for .{}'.format(fileExtension))
