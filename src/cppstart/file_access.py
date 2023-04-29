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
    def __init__(self, root_dir=None):
        assert isinstance(root_dir, Path) or root_dir is None

        self._root_dir = root_dir if root_dir is not None else Path(".")

    def read(self, path: Path):
        with open(self._root_dir / path, "r") as f:
            return f.read()
