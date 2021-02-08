import unittest
from dbxdeploy.notebook.converter import emptyLinesRemover

class emptyLinesRemoverTest(unittest.TestCase):

    def test_forcedEndFileNewLine(self):
        code = emptyLinesRemover.remove("\n".join((
            '# MAGIC %md #### Something',    
            '',
            '# COMMAND ----------',
            '',
            '',
            '@transformation(read_csv_mask_usage, display=True)',
            'def add_column_insert_ts(df: DataFrame):',
            '    return df.withColumn("INSERT_TS", f.lit(datetime.now()))',
            '',
            '',
            '# COMMAND ----------',
            '',
            '# MAGIC %md #### Saving results to fresh table"',
        )))

        expectedResult = ("\n".join((
            '# MAGIC %md #### Something',
            '',
            '# COMMAND ----------',
            '',
            '@transformation(read_csv_mask_usage, display=True)',
            'def add_column_insert_ts(df: DataFrame):',
            '    return df.withColumn("INSERT_TS", f.lit(datetime.now()))',
            '',
            '# COMMAND ----------',
            '',
            '# MAGIC %md #### Saving results to fresh table"',
        )))

        self.assertEqual(expectedResult, code)

if __name__ == '__main__':
    unittest.main()
