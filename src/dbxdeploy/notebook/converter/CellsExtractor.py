import re
from typing import List


class CellsExtractor:
    def extract(self, original_script: str, separator_regexp: str) -> List[dict]:
        def remove_ending_spaces(cell: str):
            return re.sub(r"\n+$", "", cell)

        raw_cells = re.split(separator_regexp, original_script)
        raw_cells = list(filter(lambda raw_cell: raw_cell != "", raw_cells))
        raw_cells = list(map(remove_ending_spaces, raw_cells))

        return list(map(lambda raw_cell: {"source": raw_cell, "cell_type": "code"}, raw_cells))
