from pathlib import Path


class PoetryPathResolver:
    def __init__(self, poetry_path: str):
        self.__poetry_path = poetry_path

    def get_poetry_path(self) -> Path:
        return Path(self.__poetry_path).expanduser()
