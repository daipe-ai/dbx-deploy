from pathlib import Path, PurePosixPath
from typing import List
from jinja2 import Template
from dbxdeploy.notebook.LibsRunPreparer import LibsRunPreparer

class DbcScriptRenderer:

    def __init__(
        self,
        libsRunPreparer: LibsRunPreparer,
    ):
        self.__libsRunPreparer = libsRunPreparer

    def render(self, notebookPath: Path, template: Template, cells: List[dict], whlFilename: PurePosixPath):
        return template.render(
            resources={
                'libsRun': self.__libsRunPreparer.prepare(whlFilename),
                'metadata': {
                    'name': notebookPath.stem
                },
                'global_content_filter': {
                    'include_code': True,
                    'include_input': False,
                    'include_input_prompt': False,
                    'include_output': False,
                }
            },
            nb={'cells': cells}
        )
