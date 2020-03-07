from dbxnotebookexporter.json.formatCellContent import formatCellContent
import dbxnotebookexporter.json.JsonNotebookExporter as JsonNotebookExporterModule
import nbconvert.templates.skeleton as nbConvertSkeleton
import jinja2
import os

class JinjaTemplateLoader:

    def load(self):
        basePaths = [
            os.path.dirname(JsonNotebookExporterModule.__file__),
            nbConvertSkeleton.__path__._path[0] # pylint: disable = no-member, protected-access
        ]

        templateLoader = jinja2.FileSystemLoader(searchpath=basePaths)
        templateEnv = jinja2.Environment(loader=templateLoader)
        templateEnv.filters['formatCellContent'] = formatCellContent

        return templateEnv.get_template('json_notebook.tpl')
