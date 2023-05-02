import os
from pathlib import Path


class FileReader:
    def __init__(self, root_dir=None):
        assert isinstance(root_dir, Path) or root_dir is None

        self._root_dir = root_dir if root_dir is not None else Path(".")

    @property
    def root_directory(self) -> Path:
        return self._root_dir

    def read(self, path: Path):
        with open(self._root_dir / path, "r") as f:
            return f.read()

    def read_all(self):
        return self._recursive_read_all(self._root_dir, {})

    def _recursive_read_all(self, directory: Path, current: dict[Path, str]):
        for path in directory.iterdir():
            if path.is_file():
                current[path.relative_to(self._root_dir)] = path.read_text()
            elif path.is_dir():
                self._recursive_read_all(path, current)

        return current

    def exists(self, path: Path):
        full_path = self._root_dir / path
        return full_path.exists()


class FileReadWriter(FileReader):
    def __init__(self, root_dir: Path):
        super().__init__(root_dir)

    def write(self, things: dict[Path, str]):
        for rel_path in things:
            path = self._root_dir / rel_path
            if not path.parent.exists():
                os.makedirs(path.parent)
            path.write_text(things[rel_path])
