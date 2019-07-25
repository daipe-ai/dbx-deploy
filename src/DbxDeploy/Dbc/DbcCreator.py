from DbxNotebookExporter.Json.JsonNotebookExporter import JsonNotebookExporter
from DbxDeploy.Dbc.PathsPreparer import PathsPreparer
from DbxDeploy.Notebook.LibsNotebookCreator import LibsNotebookCreator
from DbxDeploy.Whl.PackageMetadata import PackageMetadata
import zipfile
from io import BytesIO
from pathlib import Path

class DbcCreator:

    def __init__(
        self,
        dbxProjectRoot: str,
        notebookExporter: JsonNotebookExporter,
        pathsPreparer: PathsPreparer,
        libsNotebookCreator: LibsNotebookCreator
    ):
        self.__dbxProjectRoot = dbxProjectRoot
        self.__scriptExporter = notebookExporter
        self.__pathsPreparer = pathsPreparer
        self.__libsNotebookCreator = libsNotebookCreator

    def create(self, notebookPaths: list, basePath: Path, packageMetadata: PackageMetadata, packagesToInstall: list) -> bytes:
        resources = {'libsRun': '%run {}/libs'.format(packageMetadata.version.getDbxVersionPath(self.__dbxProjectRoot))}

        inMemoryOutput = BytesIO()

        zipFile = zipfile.ZipFile(inMemoryOutput, 'w', zipfile.ZIP_DEFLATED)

        # directories must be created first, otherwise DataBricks is not able to process that zip/dbc file
        for dirPath in self.__pathsPreparer.prepare(notebookPaths):
            zipFile.writestr(dirPath + '/', '')

        for notebookPath in notebookPaths:
            script, resources = self.__scriptExporter.from_filename(str(basePath.joinpath(notebookPath)), resources)
            zipPath = '/'.join(notebookPath.parts[0:-1]) + '/' + notebookPath.stem + '.python'

            zipFile.writestr(zipPath, script)

        zipFile.writestr('src/libs.python', self.__libsNotebookCreator.create(packagesToInstall, packageMetadata))

        zipFile.close()
        inMemoryOutput.seek(0)

        return inMemoryOutput.getvalue()
