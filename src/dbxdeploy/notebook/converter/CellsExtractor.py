import re
from typing import List

class CellsExtractor:

    def extract(self, originalScript: str, separatorRegexp: str) -> List[dict]:
        def removeEndingSpaces(cell: str):
            return re.sub(r'\n+$', '', cell)

        rawCells = re.split(separatorRegexp, originalScript)
        rawCells = list(filter(lambda rawCell: rawCell != '', rawCells))
        rawCells = list(map(removeEndingSpaces, rawCells))

        return list(map(lambda rawCell: {'source': rawCell, 'cell_type': 'code'}, rawCells))
