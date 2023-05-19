from pathlib import Path


class FileInfo:
    def __init__(self, path: Path, content: str, permissions=None):
        self.path = path
        self.content = content
        self.permissions = permissions

    def __eq__(self, other):
        return isinstance(other, FileInfo) \
            and self.path == other.path \
            and self.content == other.content

    def __hash__(self):
        return hash(self.path) ^ hash(self.content)

    def __str__(self):
        return f"{self.path} ({self.permissions}): {self.content[:100]}"
