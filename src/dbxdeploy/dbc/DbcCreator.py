from logging import Logger
from pathlib import PurePosixPath, Path
from typing import List
import zipfile
from io import BytesIO
from dbxdeploy.dbc.PathsPreparer import PathsPreparer
from dbxdeploy.notebook.Notebook import Notebook
from dbxdeploy.notebook.converter.DatabricksNotebookConverter import DatabricksNotebookConverter
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException
from dbxdeploy.notebook.loader import loadNotebook

class DbcCreator:

    def __init__(
        self,
        workingDirectory: Path,
        logger: Logger,
        pathsPreparer: PathsPreparer,
        databricksNotebookConverter: DatabricksNotebookConverter,
    ):
        self.__workingDirectory = workingDirectory
        self.__logger = logger
        self.__pathsPreparer = pathsPreparer
        self.__databricksNotebookConverter = databricksNotebookConverter

    def create(self, notebooks: List[Notebook], packageFilePath: str) -> bytes:
        databricksRelativePaths = list(map(lambda notebook: notebook.databricksRelativePath, notebooks))
        rootIgnoredPathName = 'root_ignored_path'

        inMemoryOutput = BytesIO()

        zipFile = zipfile.ZipFile(inMemoryOutput, 'w', zipfile.ZIP_DEFLATED)

        # directories must be created first, otherwise DataBricks is not able to process that zip/dbc file
        for dirPath in self.__pathsPreparer.prepare(databricksRelativePaths, rootIgnoredPathName):
            zipFile.writestr(dirPath + '/', '')

        for notebook in notebooks:
            source = loadNotebook(notebook.path)

            try:
                self.__databricksNotebookConverter.validateSource(source)
            except UnexpectedSourceException:
                self.__logger.debug(f'Skipping unrecognized file {notebook.relativePath}')
                continue

            notebookSource = self.__databricksNotebookConverter.toDbcNotebook(notebook.path.stem, source, packageFilePath)
            zipPath = PurePosixPath(rootIgnoredPathName).joinpath(notebook.databricksRelativePath).with_suffix('.python')
            zipFile.writestr(str(zipPath), notebookSource)

        zipFile.close()
        inMemoryOutput.seek(0)

        zipContent = inMemoryOutput.getvalue()

        with self.__workingDirectory.joinpath('dist/notebooks.dbc').open('wb') as f:
            f.write(zipContent)

        return zipContent
