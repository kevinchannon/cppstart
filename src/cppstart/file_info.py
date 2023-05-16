from pathlib import Path


class FileInfo:
    def __init__(self, path: Path, content: str, permissions=None):
        self._path = path
        self._content = content
        self._permissions = permissions

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, new_path):
        self._path = new_path

    @property
    def content(self) -> str:
        return self._content

    @property
    def permissions(self) -> int:
        return self._permissions

    @permissions.setter
    def permissions(self, new_permissions):
        self._permissions = new_permissions

    def __eq__(self, other):
        return isinstance(other, FileInfo) \
            and self.path == other.path \
            and self.content == other.content

    def __hash__(self):
        return hash(self.path) ^ hash(self.content)

    def __str__(self):
        return f"{self.path} ({self.permissions}): {self.content[:100]}"
