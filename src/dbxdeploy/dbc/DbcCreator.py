from logging import Logger
from pathlib import PurePosixPath, Path
from typing import List
import zipfile
from io import BytesIO
from dbxdeploy.dbc.PathsPreparer import PathsPreparer
from dbxdeploy.notebook.ConverterNotFoundException import ConverterNotFoundException
from dbxdeploy.notebook.Notebook import Notebook
from dbxdeploy.notebook.ConverterResolver import ConverterResolver
from dbxdeploy.notebook.loader import loadNotebook

class DbcCreator:

    def __init__(
        self,
        workingDirectory: Path,
        logger: Logger,
        pathsPreparer: PathsPreparer,
        converterResolver: ConverterResolver
    ):
        self.__workingDirectory = workingDirectory
        self.__logger = logger
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
            source = loadNotebook(notebook.path)
            zipPath = '/'.join(notebook.relativePath.parts[0:-1]) + '/' + notebook.relativePath.stem + '.python'

            try:
                converter = self.__converterResolver.resolve(notebook.path, source)
            except ConverterNotFoundException:
                self.__logger.debug(f'Skipping unrecognized file {notebook.relativePath}')
                continue

            notebookSource = converter.toDbcNotebook(notebook.path.stem, source, whlFilename)
            zipFile.writestr(zipPath, notebookSource)

        zipFile.close()
        inMemoryOutput.seek(0)

        zipContent = inMemoryOutput.getvalue()

        with self.__workingDirectory.joinpath('dist/notebooks.dbc').open('wb') as f:
            f.write(zipContent)

        return zipContent
