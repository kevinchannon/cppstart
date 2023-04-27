import os
from pathlib import Path


class FileWriter:
    def write(self, things: dict[Path, str]):
        for path in things:
            if not path.parent.exists():
                os.makedirs(path.parent)
            path.write_text(things[path])
