from DbxDeploy.Setup.PackageMetadata import PackageMetadata
from DbxDeploy.Notebook.LibsCellCreator import LibsCellCreator
import jinja2
import os

class LibsNotebookCreator:

    def __init__(self, libsCellCreator: LibsCellCreator):
        self.__libsCellCreator = libsCellCreator

    def create(self, packagesToInstall: list, packageMetadata: PackageMetadata):
        libsCode = self.__libsCellCreator.create(packagesToInstall, packageMetadata)

        templateLoader = jinja2.FileSystemLoader(searchpath=os.path.dirname(__file__))
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template('libs.python.tpl')
        outputText = template.render({'libs': libsCode.replace('\n', '\\n')})

        return outputText
