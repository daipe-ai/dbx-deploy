from abc import ABC, abstractmethod


class NotebookConverterInterface(ABC):
    @abstractmethod
    def validate_source(self, source: str):
        pass

    @abstractmethod
    def from_dbc_notebook(self, content: dict) -> str:
        pass

    @abstractmethod
    def to_dbc_notebook(self, notebook_name: str, source: str, package_file_path: str, dependencies_dir_path: str) -> str:
        pass

    @abstractmethod
    def to_workspace_import_notebook(self, source: str, package_file_path: str, dependencies_dir_path: str) -> str:
        pass
