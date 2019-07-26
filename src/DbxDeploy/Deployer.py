from DbxDeploy.Whl.WhlUploader import WhlUploader
from DbxDeploy.Setup.SetupInterface import SetupInterface
from DbxDeploy.Dbc.DbcCreator import DbcCreator
from DbxDeploy.Dbc.DbcUploader import DbcUploader
import importlib.util
from pathlib import Path
import requirements

class Deployer:

    def __init__(self,
        whlUploader: WhlUploader,
        dbcCreator: DbcCreator,
        dbcUploader: DbcUploader,
    ):
        self.__whlUploader = whlUploader
        self.__dbcCreator = dbcCreator
        self.__dbcUploader = dbcUploader

    def deploy(self, projectBasePath: Path, requirementsFilePath: Path):
        print('Building WHL package')
        print('-------------------------')

        packageMetadata = self.__loadSetup(projectBasePath).build(projectBasePath)

        whlFileName = '{}-{}-py3-none-any.whl'.format(packageMetadata.getWhlPackageName(), packageMetadata.version.getWhlVersion())

        print('Uploading WHL package')
        print('-------------------------')

        whlFilePath = projectBasePath.joinpath(Path('dist/' + whlFileName))

        with open(str(whlFilePath), mode='rb') as file:
            self.__whlUploader.upload(file.read(), whlFileName)

        print('Building notebooks into DBC package')
        print('-------------------------')

        notebookPaths = []

        for path in projectBasePath.joinpath('src').glob('**/*.ipynb'):
            notebookPaths.append(path.relative_to(projectBasePath))

        with open(str(requirementsFilePath), 'r') as requirementsFile:
            packagesToInstall = list(map(lambda req: (req.name, req.specs[0][1]), requirements.parse(requirementsFile)))

            dbcContent = self.__dbcCreator.create(
                notebookPaths,
                projectBasePath,
                packageMetadata,
                packagesToInstall
            )

        print('Uploading DBC package')
        print('-------------------------')

        self.__dbcUploader.upload(dbcContent, packageMetadata.version)

        print('Done')

    def __loadSetup(self, projectBasePath) -> SetupInterface:
        spec = importlib.util.spec_from_file_location('build', '{}/setup.py'.format(projectBasePath))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module.Setup()
