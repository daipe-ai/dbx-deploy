from dbxnotebookexporter.json.formatCellContent import formatCellContent
import dbxnotebookexporter.json.JsonNotebookExporter as JsonNotebookExporterModule
import nbconvert.templates.skeleton as nb_convert_skeleton
import jinja2
import os


class JinjaTemplateLoader:
    def load(self):
        base_paths = [
            os.path.dirname(JsonNotebookExporterModule.__file__),
            nb_convert_skeleton.__path__._path[0],
        ]

        template_loader = jinja2.FileSystemLoader(searchpath=base_paths)
        template_env = jinja2.Environment(loader=template_loader)
        template_env.filters["formatCellContent"] = formatCellContent

        return template_env.get_template("json_notebook.tpl")
