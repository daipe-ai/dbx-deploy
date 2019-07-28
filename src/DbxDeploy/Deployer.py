from DbxDeploy.Setup.SetupLoader import SetupLoader
from DbxDeploy.Setup.SetupBuilder import SetupBuilder
from DbxDeploy.Whl.WhlUploader import WhlUploader
from DbxDeploy.Dbc.DbcCreator import DbcCreator
from DbxDeploy.Dbc.DbcUploader import DbcUploader
from DbxDeploy.Whl.PackageMetadata import PackageMetadata
from pathlib import Path
import requirements

class Deployer:

    def __init__(
        self,
        projectBasePath: str,
        requirementsFilePath: str,
        setupLoader: SetupLoader,
        setupBuilder: SetupBuilder,
        whlUploader: WhlUploader,
        dbcCreator: DbcCreator,
        dbcUploader: DbcUploader,
    ):
        self.__projectBasePath = Path(projectBasePath)
        self.__requirementsFilePath = Path(requirementsFilePath)
        self.__setupLoader = setupLoader
        self.__setupBuilder = setupBuilder
        self.__whlUploader = whlUploader
        self.__dbcCreator = dbcCreator
        self.__dbcUploader = dbcUploader

    def deploy(self) -> PackageMetadata:
        print('Building WHL package')

        setup = self.__setupLoader.load(self.__projectBasePath)
        packageMetadata = self.__setupBuilder.build(setup, self.__projectBasePath)

        whlFileName = '{}-{}-py3-none-any.whl'.format(packageMetadata.getWhlPackageName(), packageMetadata.version.getWhlVersion())

        print('Uploading WHL package')

        whlFilePath = self.__projectBasePath.joinpath(Path('dist/' + whlFileName))

        with whlFilePath.open('rb') as file:
            self.__whlUploader.upload(file.read(), whlFileName)

        print('Building notebooks into DBC package')

        notebookPaths = []

        for path in self.__projectBasePath.joinpath('src').glob('**/*.ipynb'):
            notebookPaths.append(path.relative_to(self.__projectBasePath))

        with self.__requirementsFilePath.open('r', encoding='utf-8') as requirementsFile:
            packagesToInstall = list(map(lambda req: (req.name, req.specs[0][1]), requirements.parse(requirementsFile)))

            dbcContent = self.__dbcCreator.create(
                notebookPaths,
                self.__projectBasePath,
                packageMetadata,
                packagesToInstall
            )

        self.__dbcUploader.upload(dbcContent, packageMetadata.version)

        print('Deployment finished')

        return packageMetadata
