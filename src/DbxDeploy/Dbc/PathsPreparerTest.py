import unittest
from pathlib import Path
from DbxDeploy.Dbc.PathsPreparer import PathsPreparer

class PathsPreparerTest(unittest.TestCase):

    def setUp(self):
        self.__pathsPreparer = PathsPreparer()

    def test_basic(self):
        paths = [
            Path('DataSenticsLib/Ahoj/notebook_spark2.ipynb'),
            Path('DataSenticsLib/Example/notebook_spark.ipynb'),
            Path('DataSenticsLib/Example/notebook_spark3.ipynb'),
            Path('DataSenticsLib/Example/SubExample/notebook_pandas.ipynb')
        ]

        uniquePaths = self.__pathsPreparer.prepare(paths)

        self.assertListEqual([
            'DataSenticsLib',
            'DataSenticsLib/Ahoj',
            'DataSenticsLib/Example',
            'DataSenticsLib/Example/SubExample',
        ], uniquePaths)

if __name__ == '__main__':
    unittest.main()
