import os
from pathlib import Path

class WorkingDirectoryPathFactory:

    def create(self):
        return Path(os.getcwd())
