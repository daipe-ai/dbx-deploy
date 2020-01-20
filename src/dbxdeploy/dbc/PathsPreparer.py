from pathlib import Path
from typing import List

class PathsPreparer:

    def prepare(self, notebookPaths: List[Path]):
        paths = list(map(lambda notebookPath: notebookPath.parts[0:-1], notebookPaths))
        paths = list(set(paths))

        for path in paths:
            for i in range(len(path) - 1):
                x = path[0:i + 1]
                paths.append(x)

        uniquePaths = list(set(paths))
        uniquePaths = sorted(uniquePaths, key=len)

        return list(map('/'.join, uniquePaths))
