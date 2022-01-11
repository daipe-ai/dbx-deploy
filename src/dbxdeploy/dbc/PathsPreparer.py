from pathlib import PurePosixPath
from typing import List


class PathsPreparer:
    def prepare(self, databricks_relative_paths: List[PurePosixPath], root_ignored_path_name: str):
        def create_notebook_path(databricks_relative_path: PurePosixPath) -> tuple:
            return (root_ignored_path_name,) + databricks_relative_path.parts[0:-1]

        paths = list(map(create_notebook_path, databricks_relative_paths))
        paths = list(set(paths))

        for path in paths:
            for i in range(len(path) - 1):
                path_converted = path[0 : i + 1]
                paths.append(path_converted)

        unique_paths = list(set(paths))
        unique_paths = sorted(unique_paths, key=len)

        return list(map("/".join, unique_paths))
