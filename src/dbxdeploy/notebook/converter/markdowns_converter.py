import re


def to_databricks_markdown(source: str):
    markdowns_fixed = source.replace("# %% [markdown]", "# %%\n%md")
    blocks_split = re.split(r"# %%\n+", markdowns_fixed)
    converted_list = []
    for line in blocks_split:
        if line.startswith("%md"):
            line = re.sub(r"\n# |\n#", r"\n", line)
            converted_list.append(line)
        else:
            converted_list.append(line)

    return "# %%\n".join(converted_list)


def to_jupyter_markdown(source: str) -> str:
    magic_removed = source.replace("# MAGIC ", "# ")
    magic_removed = magic_removed.replace("# MAGIC", "#")
    empty_lines_removed = magic_removed.replace("# %%\n\n", "# %%\n")
    lines = empty_lines_removed.split("\n")
    processed_file = []
    for index, line in enumerate(lines):
        if line.startswith("# %md"):
            if line.__len__() > 5:
                markdown_separated = "#" + line[5:]
                lines.insert(index + 1, markdown_separated)
            if index > 0 and lines[index - 1] == "# %%":
                previous_value = lines[index - 1]
                previous_value_replaced = previous_value.replace("# %%", "# %% [markdown]")
                processed_file = processed_file[:-1]
                processed_file.append(previous_value_replaced)
        else:
            processed_file.append(line)

    return "\n".join(processed_file)
