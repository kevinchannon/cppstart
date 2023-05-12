from pathlib import Path
from file_access import *
from file_info import FileInfo


class Generator:
    def __init__(self, replacements:  dict[str, str], template_reader: FileReader):
        self._replacements = replacements
        self._template_reader = template_reader

    def run(self) -> list[FileInfo]:
        templates = self._template_reader.read_all()
        output = []
        for file in templates:
            content = file.content
            for before, after in self._replacements.items():
                content = content.replace(before, after)

            output.append(FileInfo(file.path, content))

        return output
