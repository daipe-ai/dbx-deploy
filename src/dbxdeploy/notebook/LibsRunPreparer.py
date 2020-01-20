from pathlib import PurePosixPath

class LibsRunPreparer:

    def prepare(self, whlFilename: PurePosixPath):
        return 'dbutils.library.install(\'{}\')'.format(whlFilename)
