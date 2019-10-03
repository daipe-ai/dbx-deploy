from pathlib import Path
from typing import List
from DbxDeploy.Notebook.Notebook import Notebook

class NotebooksLocator:

    def __init__(
        self,
        projectBasePath: str,
    ):
        self.__projectBasePath = Path(projectBasePath)

    def locate(self) -> List[Notebook]:
        notebooks = []

        basePath = self.__projectBasePath.joinpath('src') # type: Path

        for path in basePath.glob('**/*.ipynb'):
            notebook = Notebook(
                path,
                path.relative_to(self.__projectBasePath),
                path.relative_to(self.__projectBasePath).relative_to('src').with_suffix('').as_posix()
            )
            notebooks.append(notebook)

        return notebooks
