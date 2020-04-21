from dbxdeploy.notebook.NotebooksLocator import NotebooksLocator
from dbxdeploy.package.PackageMetadata import PackageMetadata
from dbxdeploy.notebook.NotebooksDeployer import NotebooksDeployer

class CurrentAndReleaseDeployer:

    def __init__(
        self,
        notebooksLocator: NotebooksLocator,
        notebooksDeployer: NotebooksDeployer,
    ):
        self.__notebooksLocator = notebooksLocator
        self.__notebooksDeployer = notebooksDeployer

    def deploy(self, packageMetadata: PackageMetadata):
        notebooks = self.__notebooksLocator.locate()

        self.__notebooksDeployer.deploy(packageMetadata, notebooks)

    def release(self, packageMetadata: PackageMetadata):
        notebooks = self.__notebooksLocator.locate()

        self.__notebooksDeployer.release(packageMetadata, notebooks)
