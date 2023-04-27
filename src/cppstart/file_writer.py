from pathlib import Path


class FileWriter:
    def write(self, things: dict[Path, str]):
        for path in things:
            path.write_text(things[path])
