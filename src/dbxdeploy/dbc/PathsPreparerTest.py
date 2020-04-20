import unittest
from pathlib import PurePosixPath
from dbxdeploy.dbc.PathsPreparer import PathsPreparer

class PathsPreparerTest(unittest.TestCase):

    def setUp(self):
        self.__pathsPreparer = PathsPreparer()

    def test_basic(self):
        paths = [
            PurePosixPath('DataSenticsLib/Ahoj/notebook_spark2.ipynb'),
            PurePosixPath('DataSenticsLib/Example/notebook_spark.ipynb'),
            PurePosixPath('DataSenticsLib/Example/notebook_spark3.ipynb'),
            PurePosixPath('DataSenticsLib/Example/SubExample/notebook_pandas.ipynb')
        ]

        uniquePaths = sorted(self.__pathsPreparer.prepare(paths, 'root_ignored_path'))

        self.assertListEqual([
            'root_ignored_path',
            'root_ignored_path/DataSenticsLib',
            'root_ignored_path/DataSenticsLib/Ahoj',
            'root_ignored_path/DataSenticsLib/Example',
            'root_ignored_path/DataSenticsLib/Example/SubExample',
        ], uniquePaths)

if __name__ == '__main__':
    unittest.main()
