from consolebundle.ConsoleBundle import ConsoleBundle
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.container.ContainerInterface import ContainerInterface
from injecta.package.pathResolver import resolvePath
from typing import List
from pyfony.PyfonyBundle import PyfonyBundle
from pyfony.kernel.BaseKernel import BaseKernel
from pyfonybundles.Bundle import Bundle
from dbxdeploy.DbxDeployBundle import DbxDeployBundle

def initContainer(appEnv) -> ContainerInterface:
    class Kernel(BaseKernel):

        def _registerBundles(self) -> List[Bundle]:
            return [
                PyfonyBundle(),
                ConsoleBundle(),
                DbxDeployBundle()
            ]

    kernel = Kernel(
        appEnv,
        resolvePath('dbxdeploy') + '/_config',
        YamlConfigReader()
    )

    return kernel.initContainer()
