import json
import zipfile
from pyfonycore import pyproject
from pyfonycore.bootstrap.config.raw import rawConfigReader
from pathlib import Path

class BootstrapConfigAppender:

    def append(self, packagePath: Path):
        packageFileName = packagePath.stem
        packageFileNameParts = packageFileName.split('-')
        packageFileName = packageFileNameParts[0].replace('__', '_') # __myproject__ needs to be converted to _myproject_ for some reason

        distInfoDir = f'{packageFileName}-{packageFileNameParts[1]}.dist-info'

        zipFile = zipfile.ZipFile(packagePath, 'a')
        zipFile.writestr(distInfoDir + '/entry_points.txt', self.__prepareEntryPoints())
        zipFile.writestr(distInfoDir + '/bootstrap_config.json', self.__prepareBootstrapConfig())
        zipFile.close()

    def __prepareEntryPoints(self):
        return '[pyfony.bootstrap]\nfoo=bar\n'

    def __prepareBootstrapConfig(self):
        bootstrapConfig = rawConfigReader.read(pyproject.getPath())
        return json.dumps(bootstrapConfig)
