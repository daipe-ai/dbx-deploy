import sys
import shutil
from pathlib import Path
from dbxdeploy.package.BootstrapConfigAppender import BootstrapConfigAppender
from dbxdeploy.package.LockedPyprojectCreator import LockedPyprojectCreator
from dbxdeploy.package.PackageMetadata import PackageMetadata
from dbxdeploy.deploy.LocalPathsResolver import LocalPathsResolver
from dbxdeploy.poetry.PoetryPathResolver import PoetryPathResolver
from dbxdeploy.shell.runner import runShellCommand
from dbxdeploy.filesystem.utils import deleteDirectoryContentRecursive

class PackageBuilder:

    def __init__(
        self,
        projectBaseDir: Path,
        offlineInstall: bool,
        lockedPyprojectCreator: LockedPyprojectCreator,
        bootstrapConfigAppender: BootstrapConfigAppender,
        localPathsResolver: LocalPathsResolver,
        poetryPathResolver: PoetryPathResolver,
    ):
        self.__projectBaseDir = projectBaseDir
        self.__offlineInstall = offlineInstall
        self.__lockedPyprojectCreator = lockedPyprojectCreator
        self.__bootstrapConfigAppender = bootstrapConfigAppender
        self.__localPathsResolver = localPathsResolver
        self.__poetryPathResolver = poetryPathResolver

    def build(self, basePath: Path, packageMetadata: PackageMetadata):
        distDir = basePath.joinpath('dist')

        deleteDirectoryContentRecursive(distDir)

        pyprojectOrigPath = basePath.joinpath('pyproject.toml')
        pyprojectNewPath = basePath.joinpath('pyproject.toml.new')

        self.__lockedPyprojectCreator.create(basePath, pyprojectOrigPath, pyprojectNewPath)

        packageFileName = packageMetadata.getPackageFilename()
        packagePath = self.__projectBaseDir.joinpath(Path('dist')).joinpath(packageFileName)

        self.__buildWheel(pyprojectOrigPath, pyprojectNewPath, basePath)

        self.__bootstrapConfigAppender.append(packagePath)

        if self.__offlineInstall:
            self.__buildWheelhouse(basePath, packageMetadata)

    def __buildWheel(self, pyprojectOrigPath: Path, pyprojectNewPath: Path, basePath: Path):
        pyprojectDist = basePath.joinpath('dist/pyproject.toml')
        pyprojectBakPath = basePath.joinpath('pyproject.toml.bak')

        pyprojectOrigPath.rename(pyprojectBakPath)
        pyprojectNewPath.rename(pyprojectOrigPath)

        pythonExecutable = sys.executable
        poetryPath = self.__poetryPathResolver.getPoetryPath()

        try:
            runShellCommand(f'{pythonExecutable} {poetryPath} build --format wheel', cwd=str(basePath), shell=True)
        except BaseException: # pylint: disable = broad-except
            pass
        finally:
            pyprojectOrigPath.replace(pyprojectDist)
            pyprojectBakPath.rename(pyprojectOrigPath)

    def __buildWheelhouse(self, basePath: Path, packageMetadata: PackageMetadata):
        dependenciesDir = basePath.joinpath('dependencies')
        distDir = basePath.joinpath('dist')

        if not dependenciesDir.is_dir():
            raise Exception(f'Cannot find dependencies dir at {dependenciesDir}')

        for dependency in packageMetadata.dependencies:
            dependencyWheel = self.__localPathsResolver.getLinuxDependencyPathFromDir(dependenciesDir, dependency)

            shutil.copy(dependencyWheel, distDir)
