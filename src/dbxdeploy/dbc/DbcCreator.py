from pathlib import PurePosixPath
from typing import List
from dbxdeploy.dbc.PathsPreparer import PathsPreparer
from dbxdeploy.notebook.Notebook import Notebook
from dbxdeploy.notebook.ConverterResolver import ConverterResolver
import zipfile
from io import BytesIO

class DbcCreator:

    def __init__(
        self,
        pathsPreparer: PathsPreparer,
        converterResolver: ConverterResolver
    ):
        self.__pathsPreparer = pathsPreparer
        self.__converterResolver = converterResolver

    def create(self, notebooks: List[Notebook], whlFilename: PurePosixPath) -> bytes:
        notebookRelativePaths = list(map(lambda notebook: notebook.relativePath, notebooks))

        inMemoryOutput = BytesIO()

        zipFile = zipfile.ZipFile(inMemoryOutput, 'w', zipfile.ZIP_DEFLATED)

        # directories must be created first, otherwise DataBricks is not able to process that zip/dbc file
        for dirPath in self.__pathsPreparer.prepare(notebookRelativePaths):
            zipFile.writestr(dirPath + '/', '')

        for notebook in notebooks:
            converter = self.__converterResolver.resolve(notebook.converterClass)
            zipPath = '/'.join(notebook.relativePath.parts[0:-1]) + '/' + notebook.relativePath.stem + '.python'

            zipFile.writestr(zipPath, converter.toDbcNotebook(notebook.path, whlFilename))

        zipFile.close()
        inMemoryOutput.seek(0)

        return inMemoryOutput.getvalue()
