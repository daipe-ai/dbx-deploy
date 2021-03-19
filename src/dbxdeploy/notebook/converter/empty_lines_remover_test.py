import unittest
from dbxdeploy.notebook.converter import empty_lines_remover


class empty_lines_remover_test(unittest.TestCase):  # noqa: N801
    def test_forced_end_file_new_line(self):
        code = empty_lines_remover.remove(
            "\n".join(
                (
                    "# MAGIC %md #### Something",
                    "",
                    "# COMMAND ----------",
                    "",
                    "",
                    "@transformation(read_csv_mask_usage, display=True)",
                    "def add_column_insert_ts(df: DataFrame):",
                    '    return df.withColumn("INSERT_TS", f.lit(datetime.now()))',
                    "",
                    "",
                    "# COMMAND ----------",
                    "",
                    '# MAGIC %md #### Saving results to fresh table"',
                )
            )
        )

        expected_result = "\n".join(
            (
                "# MAGIC %md #### Something",
                "",
                "# COMMAND ----------",
                "",
                "@transformation(read_csv_mask_usage, display=True)",
                "def add_column_insert_ts(df: DataFrame):",
                '    return df.withColumn("INSERT_TS", f.lit(datetime.now()))',
                "",
                "# COMMAND ----------",
                "",
                '# MAGIC %md #### Saving results to fresh table"',
            )
        )

        self.assertEqual(expected_result, code)


if __name__ == "__main__":
    unittest.main()
