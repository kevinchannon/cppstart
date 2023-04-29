import os
from pathlib import Path


class FileWriter:
    def __init__(self, root_dir: Path):
        self._root_dir = root_dir

    @property
    def root_directory(self) -> Path:
        return self._root_dir

    def write(self, things: dict[Path, str]):
        for rel_path in things:
            path = self._root_dir / rel_path
            if not path.parent.exists():
                os.makedirs(path.parent)
            path.write_text(things[rel_path])


class FileReader:
    @staticmethod
    def read(path: Path):
        with open(path, "r") as f:
            return f.read()
