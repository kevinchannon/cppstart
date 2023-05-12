from pathlib import Path


class FileInfo:
    def __init__(self, path: Path, content: str, permissions=None):
        self._path = path
        self._content = content
        self._permissions = permissions

    @property
    def path(self) -> Path:
        return self._path

    @property
    def content(self) -> str:
        return self._content

    @property
    def permissions(self) -> int:
        return self._permissions

    def __eq__(self, other):
        return self.path == other.path and self.content == other.content and self.permissions == other.permissions
