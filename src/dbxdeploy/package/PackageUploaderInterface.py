from abc import ABC, abstractmethod


class PackageUploaderInterface(ABC):
    @abstractmethod
    def upload(self, content: bytes, file_path: str, overwrite: bool = False):
        pass

    @abstractmethod
    def exists(self, file_path: str):
        pass
