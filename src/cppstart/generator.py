from pathlib import Path
from file_access import *


class Generator:
    def __init__(self, replacements:  dict[str, str], template_reader: FileReader):
        self._replacements = replacements
        self._template_reader = template_reader

    def run(self) -> dict[Path, str]:
        templates = self._template_reader.read_all()
        output = {}
        for path, template in templates.items():
            content = template
            for before, after in self._replacements.items():
                content = content.replace(before, after)

            output[path] = content

        return output
