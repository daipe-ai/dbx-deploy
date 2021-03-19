from dbxdeploy.notebook.NotebooksLocator import NotebooksLocator
from dbxdeploy.package.PackageMetadata import PackageMetadata
from dbxdeploy.notebook.NotebooksDeployer import NotebooksDeployer


class CurrentAndReleaseDeployer:
    def __init__(
        self,
        notebooks_locator: NotebooksLocator,
        notebooks_deployer: NotebooksDeployer,
    ):
        self.__notebooks_locator = notebooks_locator
        self.__notebooks_deployer = notebooks_deployer

    def deploy(self, package_metadata: PackageMetadata):
        notebooks = self.__notebooks_locator.locate()

        self.__notebooks_deployer.deploy(package_metadata, notebooks)

    def release(self, package_metadata: PackageMetadata):
        notebooks = self.__notebooks_locator.locate()

        self.__notebooks_deployer.release(package_metadata, notebooks)

    def deploy_only_master_package_notebook(self, package_metadata: PackageMetadata):
        master_package_notebook = self.__notebooks_locator.locate_master_package_notebook()

        self.__notebooks_deployer.deploy_only_master_package_notebook(package_metadata, master_package_notebook)
