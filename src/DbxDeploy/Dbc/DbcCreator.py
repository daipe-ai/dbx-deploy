from DbxNotebookExporter.Json.JsonNotebookExporter import JsonNotebookExporter
from DbxDeploy.Dbc.PathsPreparer import PathsPreparer
from DbxDeploy.Setup.PackageMetadata import PackageMetadata
import zipfile
from io import BytesIO
from pathlib import Path

class DbcCreator:

    def __init__(
        self,
        whlBasePath: str,
        notebookExporter: JsonNotebookExporter,
        pathsPreparer: PathsPreparer
    ):
        self.__whlBasePath = whlBasePath
        self.__scriptExporter = notebookExporter
        self.__pathsPreparer = pathsPreparer

    def create(self, notebookPaths: list, basePath: Path, packageMetadata: PackageMetadata) -> bytes:
        whlFilename = self.__whlBasePath + '/' + packageMetadata.getWhlFileName()

        resources = {'libsRun': 'dbutils.library.install(\'{}\')'.format(whlFilename)}

        inMemoryOutput = BytesIO()

        zipFile = zipfile.ZipFile(inMemoryOutput, 'w', zipfile.ZIP_DEFLATED)

        # directories must be created first, otherwise DataBricks is not able to process that zip/dbc file
        for dirPath in self.__pathsPreparer.prepare(notebookPaths):
            zipFile.writestr(dirPath + '/', '')

        for notebookPath in notebookPaths:
            script, resources = self.__scriptExporter.from_filename(str(basePath.joinpath(notebookPath)), resources)
            zipPath = '/'.join(notebookPath.parts[0:-1]) + '/' + notebookPath.stem + '.python'

            zipFile.writestr(zipPath, script)

        zipFile.close()
        inMemoryOutput.seek(0)

        return inMemoryOutput.getvalue()
