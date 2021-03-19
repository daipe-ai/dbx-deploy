import os
from pathlib import Path


class WorkingDirFactory:
    def create(self):
        return Path(os.getcwd())
