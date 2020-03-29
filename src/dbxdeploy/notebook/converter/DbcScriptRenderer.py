from typing import List
from jinja2 import Template

class DbcScriptRenderer:

    def render(self, notebookName: str, template: Template, cells: List[dict]):
        resources = {
            'metadata': {
                'name': notebookName,
            },
            'global_content_filter': {
                'include_code': True,
                'include_input': False,
                'include_input_prompt': False,
                'include_output': False,
            }
        }

        return template.render(
            resources=resources,
            nb={'cells': cells}
        )
