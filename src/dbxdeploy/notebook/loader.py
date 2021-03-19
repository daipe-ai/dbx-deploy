from pathlib import Path


def load_notebook(notebook_path: Path) -> str:
    with notebook_path.open("r", encoding="utf-8") as f:
        return f.read()
