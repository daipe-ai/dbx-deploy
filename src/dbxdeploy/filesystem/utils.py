import os
from pathlib import Path

def deleteDirectoryContentRecursive(dirPath: Path):
    if dirPath.is_dir():
        fileList = []
        dirList = []

        for root, dirs, files in os.walk(dirPath):
            for f in files:
                fileList.append(os.path.join(root, f))

            for d in dirs:
                dirList.append(os.path.join(root, d))

        for f in fileList:
            os.unlink(f)

        for d in dirList:
            os.rmdir(d)
