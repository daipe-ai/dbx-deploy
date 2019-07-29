from DbxDeploy.Setup.SetupLoader import SetupLoader
from DbxDeploy.Whl.WhlDeployer import WhlDeployer
from DbxDeploy.Dbc.DbcDeployer import DbcDeployer
from pathlib import Path

class Deployer:

    def __init__(
        self,
        projectBasePath: str,
        setupLoader: SetupLoader,
        dbcDeployer: DbcDeployer,
        whlDeployer: WhlDeployer,
    ):
        self.__projectBasePath = Path(projectBasePath)
        self.__setupLoader = setupLoader
        self.__dbcDeployer = dbcDeployer
        self.__whlDeployer = whlDeployer

    def deploy(self):
        setup = self.__setupLoader.load(self.__projectBasePath)
        packageMetadata = setup.getPackageMetadata()

        self.__whlDeployer.deploy(setup, packageMetadata)
        self.__dbcDeployer.deploy(packageMetadata)
