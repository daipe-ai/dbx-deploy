import re


def remove(source: str):
    source = re.sub(r"(#[\s]+COMMAND[\s]+[-]+)([\n]|[\r\n]|[\r]){3,}", "\\1\\2\\2", source, flags=re.MULTILINE)
    source = re.sub(r"([\n]|[\r\n]|[\r]){3,}(#[\s]+COMMAND[\s]+[-]+)", "\\1\\1\\2", source, flags=re.MULTILINE)

    return source
