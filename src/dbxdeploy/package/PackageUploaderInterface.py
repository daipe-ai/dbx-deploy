from abc import ABC, abstractmethod

class PackageUploaderInterface(ABC):

    @abstractmethod
    def upload(self, content: bytes, filePath: str, overwrite: bool = False):
        pass

    @abstractmethod
    def exists(self, filePath: str):
        pass
