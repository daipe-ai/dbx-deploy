import subprocess
import io
from pathlib import Path

class WhlBuilder:

    def build(self, projectBasePath: Path):
        arguments = ['poetry', 'build', '--format', 'wheel']

        proc = subprocess.Popen(arguments, stdout=subprocess.PIPE, cwd=str(projectBasePath), shell=True)
        for line in io.TextIOWrapper(proc.stdout, encoding='utf-8'):
            print(line.replace('\n', ''))
