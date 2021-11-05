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
        bootstrap_notebooks = []

        self.__notebooks_locator.check_at_least_one_bootstrap_ntb_present()

        if self.__notebooks_locator.bootstrap_notebook_present():
            bootstrap_notebooks.append(self.__notebooks_locator.locate_bootstrap_notebook())

        if self.__notebooks_locator.master_package_notebook_present():
            bootstrap_notebooks.append(self.__notebooks_locator.locate_master_package_notebook())

        self.__notebooks_deployer.deploy_only_master_package_notebook(package_metadata, bootstrap_notebooks)
