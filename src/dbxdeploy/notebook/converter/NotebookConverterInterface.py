from abc import ABC, abstractmethod
from pathlib import Path, PurePosixPath

class NotebookConverterInterface(ABC):

    @abstractmethod
    def getSupportedExtensions(self) -> list:
        pass

    @abstractmethod
    def validateSource(self, source: str):
        pass

    @abstractmethod
    def fromDbcNotebook(self, content: dict) -> str:
        pass

    @abstractmethod
    def toDbcNotebook(self, notebookName: str, source: str, whlFilename: PurePosixPath) -> str:
        pass

    @abstractmethod
    def toWorkspaceImportNotebook(self, source: str, whlFilename: PurePosixPath) -> str:
        pass

    @abstractmethod
    def getGlobPatterns(self) -> list:
        pass

    @abstractmethod
    def getConsumerGlobPatterns(self) -> list:
        pass

    @abstractmethod
    def getDescription(self) -> str:
        pass
