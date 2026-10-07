import ast
from pathlib import Path

def test_all_python_files_parse():
    for path in Path(".").rglob("*.py"):
        if ".git" in path.parts: continue
        ast.parse(path.read_text(encoding="utf-8-sig"),filename=str(path))