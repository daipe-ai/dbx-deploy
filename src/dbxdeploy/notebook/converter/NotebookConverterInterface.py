from abc import ABC, abstractmethod
from pathlib import Path, PurePosixPath

class NotebookConverterInterface(ABC):

    @abstractmethod
    def toDbcNotebook(self, notebookPath: Path, whlFilename: PurePosixPath) -> str:
        pass

    @abstractmethod
    def toWorkspaceImportNotebook(self, notebookPath: Path, whlFilename: PurePosixPath) -> str:
        pass

    @abstractmethod
    def resolves(self, fileExtension: str) -> bool:
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
