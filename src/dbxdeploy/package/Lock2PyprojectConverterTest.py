import unittest
from tomlkit import table, inline_table
from dbxdeploy.package.Lock2PyprojectConverter import Lock2PyprojectConverter

class Lock2PyprojectConverterTest(unittest.TestCase):

    def setUp(self):
        self.__lock2PyprojectConverter = Lock2PyprojectConverter()

    def test_basic(self):
        t = table()
        t.append('name', 'mypackage')
        t.append('version', '1.2.3')

        packageName, packageVersion = self.__lock2PyprojectConverter.convert(t)

        self.assertEqual('mypackage', packageName)
        self.assertEqual('1.2.3', packageVersion)

    def test_basic_withMarkers(self):
        t = table()
        t.append('name', 'mypackage')
        t.append('version', '1.2.3')
        t.append('marker', 'sys_platform == "darwin"')

        packageName, packageDefinition = self.__lock2PyprojectConverter.convert(t)

        it = inline_table()
        it.append('version', '1.2.3')
        it.append('markers', 'sys_platform == "darwin"')

        self.assertEqual('mypackage', packageName)
        self.assertEqual(it, packageDefinition)

    def test_git(self):
        t = table()
        t.append('name', 'mypackage')
        t.append('version', '1.2.3')

        tr = table()
        tr.append('reference', '0e2068c02f72b9d3092ff8343aab72cd606fc983')
        tr.append('type', 'git')
        tr.append('url', 'https://github.com/bricksflow/dbx-deploy.git')

        t.append('source', tr)

        packageName, packageDefinition = self.__lock2PyprojectConverter.convert(t)

        it = inline_table()
        it.append('git', 'https://github.com/bricksflow/dbx-deploy.git')
        it.append('rev', '0e2068c02f72b9d3092ff8343aab72cd606fc983')

        self.assertEqual('mypackage', packageName)
        self.assertEqual(it, packageDefinition)

if __name__ == '__main__':
    unittest.main()
