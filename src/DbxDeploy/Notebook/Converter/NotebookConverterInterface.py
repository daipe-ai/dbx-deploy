from abc import ABC
from pathlib import Path

class NotebookConverterInterface(ABC):

    def toDbcNotebook(self, notebookPath: Path, whlFilename: str) -> str:
        pass

    def toWorkspaceImportNotebook(self, notebookPath: Path, whlFilename: str) -> str:
        pass

    def resolves(self, fileExtension: str) -> bool:
        pass
