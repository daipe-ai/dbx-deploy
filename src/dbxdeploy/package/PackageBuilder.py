import subprocess
from pathlib import Path
from dbxdeploy.package.BootstrapConfigAppender import BootstrapConfigAppender
from dbxdeploy.package.LockedPyprojectCreator import LockedPyprojectCreator

class PackageBuilder:

    def __init__(
        self,
        projectBaseDir: Path,
        lockedPyprojectCreator: LockedPyprojectCreator,
        bootstrapConfigAppender: BootstrapConfigAppender,
    ):
        self.__projectBaseDir = projectBaseDir
        self.__lockedPyprojectCreator = lockedPyprojectCreator
        self.__bootstrapConfigAppender = bootstrapConfigAppender

    def build(self, basePath: Path, packageFileName):
        basePath.joinpath('dist').mkdir(exist_ok=True)

        lockfilePath = basePath.joinpath('poetry.lock')
        pyprojectOrigPath = basePath.joinpath('pyproject.toml')
        pyprojectNewPath = basePath.joinpath('pyproject.toml.new')

        self.__lockedPyprojectCreator.create(lockfilePath, pyprojectOrigPath, pyprojectNewPath)

        packagePath = self.__projectBaseDir.joinpath(Path('dist')).joinpath(packageFileName)

        self.__buildWheel(pyprojectOrigPath, pyprojectNewPath, basePath)

        self.__bootstrapConfigAppender.append(packagePath)

        return packagePath

    def __buildWheel(self, pyprojectOrigPath: Path, pyprojectNewPath: Path, basePath: Path):
        pyprojectDist = basePath.joinpath('dist/pyproject.toml')
        pyprojectBakPath = basePath.joinpath('pyproject.toml.bak')

        pyprojectOrigPath.rename(pyprojectBakPath)
        pyprojectNewPath.rename(pyprojectOrigPath)

        try:
            subprocess.run('poetry build --format wheel', check=True, cwd=str(basePath), shell=True)
        except BaseException: # pylint: disable = broad-except
            pass
        finally:
            pyprojectOrigPath.replace(pyprojectDist)
            pyprojectBakPath.rename(pyprojectOrigPath)
