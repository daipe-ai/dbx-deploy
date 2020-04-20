from pathlib import PurePosixPath
from typing import List

class PathsPreparer:

    def prepare(self, databricksRelativePaths: List[PurePosixPath], rootIgnoredPathName: str):
        def createNotebookPath(databricksRelativePath: PurePosixPath) -> tuple:
            return (rootIgnoredPathName, ) + databricksRelativePath.parts[0:-1]

        paths = list(map(createNotebookPath, databricksRelativePaths))
        paths = list(set(paths))

        for path in paths:
            for i in range(len(path) - 1):
                x = path[0:i + 1]
                paths.append(x)

        uniquePaths = list(set(paths))
        uniquePaths = sorted(uniquePaths, key=len)

        return list(map('/'.join, uniquePaths))
