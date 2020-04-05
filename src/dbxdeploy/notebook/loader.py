from pathlib import Path

def loadNotebook(notebookPath: Path) -> str:
    with notebookPath.open('r', encoding='utf-8') as f:
        return f.read()
