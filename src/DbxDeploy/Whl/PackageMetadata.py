import setuptools.dist
from DbxDeploy.Setup.Version.VersionInterface import VersionInterface

class PackageMetadata:

    def __init__(
        self,
        packageName: str,
        version: VersionInterface,
        distribution: setuptools.dist.Distribution
    ):
        self.packageName = packageName
        self.version = version
        self.distribution = distribution

    def getWhlPackageName(self):
        return self.packageName.replace('-', '_')
