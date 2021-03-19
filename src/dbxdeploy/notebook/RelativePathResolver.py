from pathlib import PurePosixPath


class RelativePathResolver:
    def __init__(
        self,
        base_dir_path: str,
    ):
        self.__base_dir_path = base_dir_path

    def resolve(self, notebook_path: PurePosixPath):
        return notebook_path.relative_to(self.__base_dir_path).with_suffix("")
