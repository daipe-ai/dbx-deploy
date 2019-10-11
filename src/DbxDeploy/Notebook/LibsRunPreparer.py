from pathlib import PurePosixPath

class LibsRunPreparer:

    def __init__(
        self,
        whlBasePath: str,
    ):
        self.__whlBasePath = PurePosixPath(whlBasePath)

    def prepare(self, whlFilename: str):
        whlFilename = self.__whlBasePath.joinpath(whlFilename)

        return 'dbutils.library.install(\'{}\')'.format(whlFilename)
