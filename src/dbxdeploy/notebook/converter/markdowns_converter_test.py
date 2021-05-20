import unittest
from dbxdeploy.notebook.converter import markdowns_converter


class markdowns_converter_test(unittest.TestCase):  # noqa: N801
    def test_to_databricks_markdown_converter(self):
        code = markdowns_converter.to_databricks_markdown(
            "\n".join(
                (
                    "# %% [markdown]",
                    "# ##TEST",
                    "",
                    "# %%",
                    "@transformation(read_csv_mask_usage, display=True)",
                    "def add_column_insert_ts(df: DataFrame):",
                    '    return df.withColumn("INSERT_TS", f.lit(datetime.now()))',
                    "",
                    "# %% [markdown]",
                    '# #### Saving results to fresh table"',
                )
            )
        )

        expected_result = "\n".join(
            (
                "# %%",
                "%md",
                "##TEST",
                "",
                "# %%",
                "@transformation(read_csv_mask_usage, display=True)",
                "def add_column_insert_ts(df: DataFrame):",
                '    return df.withColumn("INSERT_TS", f.lit(datetime.now()))',
                "",
                "# %%",
                "%md",
                '#### Saving results to fresh table"',
            )
        )

        self.assertEqual(expected_result, code)

    def test_to_jupyter_md_on_first_line(self):
        code = markdowns_converter.to_jupyter_markdown(
            "\n".join(
                (
                    "# %%",
                    "# %md",
                    "# ##TEST",
                    "",
                    "# %%",
                    "@transformation(read_csv_mask_usage, display=True)",
                    "def add_column_insert_ts(df: DataFrame):",
                    '    return df.withColumn("INSERT_TS", f.lit(datetime.now()))',
                    "",
                    "# %%",
                    "# %md",
                    '# #### Saving results to fresh table"',
                )
            )
        )

        expected_result = "\n".join(
            (
                "# %% [markdown]",
                "# ##TEST",
                "",
                "# %%",
                "@transformation(read_csv_mask_usage, display=True)",
                "def add_column_insert_ts(df: DataFrame):",
                '    return df.withColumn("INSERT_TS", f.lit(datetime.now()))',
                "",
                "# %% [markdown]",
                '# #### Saving results to fresh table"',
            )
        )

        self.assertEqual(expected_result, code)

    def test_to_jupyter_md_on_second_line(self):
        code = markdowns_converter.to_jupyter_markdown(
            "\n".join(
                (
                    "# %%",
                    "",
                    "# %md",
                    "# ##TEST",
                    "",
                    "# %%",
                    "@transformation(read_csv_mask_usage, display=True)",
                    "def add_column_insert_ts(df: DataFrame):",
                    '    return df.withColumn("INSERT_TS", f.lit(datetime.now()))',
                    "",
                    "# %%",
                    "",
                    "# %md",
                    '# #### Saving results to fresh table"',
                )
            )
        )

        expected_result = "\n".join(
            (
                "# %% [markdown]",
                "# ##TEST",
                "",
                "# %%",
                "@transformation(read_csv_mask_usage, display=True)",
                "def add_column_insert_ts(df: DataFrame):",
                '    return df.withColumn("INSERT_TS", f.lit(datetime.now()))',
                "",
                "# %% [markdown]",
                '# #### Saving results to fresh table"',
            )
        )

        self.assertEqual(expected_result, code)

    def test_to_jupyter_md_with_comment_on_one_line(self):
        code = markdowns_converter.to_jupyter_markdown(
            "\n".join(
                (
                    "# %%",
                    "",
                    "# %md ##TEST",
                    "",
                    "# %%",
                    "@transformation(read_csv_mask_usage, display=True)",
                    "def add_column_insert_ts(df: DataFrame):",
                    '    return df.withColumn("INSERT_TS", f.lit(datetime.now()))',
                    "",
                    "# %%",
                    "",
                    "# %md #### Saving results to fresh table",
                )
            )
        )

        expected_result = "\n".join(
            (
                "# %% [markdown]",
                "# ##TEST",
                "",
                "# %%",
                "@transformation(read_csv_mask_usage, display=True)",
                "def add_column_insert_ts(df: DataFrame):",
                '    return df.withColumn("INSERT_TS", f.lit(datetime.now()))',
                "",
                "# %% [markdown]",
                "# #### Saving results to fresh table",
            )
        )

        self.assertEqual(expected_result, code)


if __name__ == "__main__":
    unittest.main()
