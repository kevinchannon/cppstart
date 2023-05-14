import os
from pathlib import Path

from file_info import FileInfo


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

    def read_all(self) -> set[FileInfo]:
        return self._recursive_read_all(self._root_dir, set())

    def _recursive_read_all(self, directory: Path, current: set[FileInfo]) -> set[FileInfo]:
        for path in directory.iterdir():
            if path.is_file():
                permissions = os.stat(path).st_mode & 0o777
                current.add(
                    FileInfo(path=path.relative_to(self._root_dir), content=path.read_text(), permissions=permissions))
            elif path.is_dir():
                self._recursive_read_all(path, current)

        return current

    def exists(self, path: Path):
        full_path = self._root_dir / path
        return full_path.exists()


class FileReadWriter(FileReader):
    def __init__(self, root_dir: Path):
        super().__init__(root_dir)

    def write(self, things: set[FileInfo]):
        for file_info in things:
            path = self._root_dir / file_info.path
            if not path.parent.exists():
                os.makedirs(path.parent)
            path.write_text(file_info.content)

            if file_info.permissions is not None:
                os.chmod(path, file_info.permissions)
