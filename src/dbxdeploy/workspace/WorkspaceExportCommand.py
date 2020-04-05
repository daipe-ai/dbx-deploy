import json
from argparse import Namespace
from pathlib import PurePosixPath, Path
from zipfile import ZipInfo, ZipFile
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.notebook.ConverterResolver import ConverterResolver
from dbxdeploy.notebook.loader import loadNotebook
from dbxdeploy.workspace.DbcFilesHandler import DbcFilesHandler
from dbxdeploy.workspace.WorkspaceExporter import WorkspaceExporter

class WorkspaceExportCommand(ConsoleCommand):

    def __init__(
        self,
        dbxProjectRoot: PurePosixPath,
        projectBasePath: Path,
        workspaceExporter: WorkspaceExporter,
        dbcFilesHandler: DbcFilesHandler,
        converterResolver: ConverterResolver,
    ):
        self.__dbxProjectRoot = dbxProjectRoot
        self.__projectBasePath = projectBasePath
        self.__workspaceExporter = workspaceExporter
        self.__dbcFilesHandler = dbcFilesHandler
        self.__converterResolver = converterResolver

    def getCommand(self) -> str:
        return 'dbx:workspace:export'

    def getDescription(self):
        return 'Export notebooks from Databricks workspace to local project'

    def run(self, inputArgs: Namespace):
        def readFile(zipFile: ZipFile, file: ZipInfo):
            if file.orig_filename[-1:] == '/':
                return

            filePathWithoutRootdir = file.orig_filename[file.orig_filename.index('/') + 1:file.orig_filename.rindex('.')] + '.py'
            localFilePath = self.__projectBasePath.joinpath('src').joinpath(filePathWithoutRootdir)

            localFileSource = loadNotebook(localFilePath)
            converter = self.__converterResolver.resolve(localFilePath, localFileSource)

            with localFilePath.open('wb') as f:
                zippedFileContent = zipFile.read(file.orig_filename).decode('utf-8')
                pyContent = converter.fromDbcNotebook(json.loads(zippedFileContent))

                f.write(pyContent.encode('utf-8'))

        dbcContent = self.__workspaceExporter.export(self.__dbxProjectRoot)
        self.__dbcFilesHandler.handle(dbcContent, readFile)
