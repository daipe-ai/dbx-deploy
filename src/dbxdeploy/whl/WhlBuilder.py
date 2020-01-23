import subprocess
from pathlib import Path

class WhlBuilder:

    def build(self, projectBasePath: Path):
        arguments = ['poetry', 'build', '--format', 'wheel']

        subprocess.run(arguments, check=True, cwd=str(projectBasePath))
