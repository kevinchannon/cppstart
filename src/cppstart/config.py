import configparser
from pathlib import Path

from file_access import FileReader


class Config:
    def __init__(self, file_reader: FileReader):
        self._parser = configparser.ConfigParser()
        self._file_reader = file_reader

    def read(self, path: Path):
        config_str = self._file_reader.read(path)
        self._parser.read_string(config_str)

    def get(self, section: str, item: str):
        return self._parser.get(section, item)

    def set(self, section: str, item: str, value):
        if not self._parser.has_section(section):
            self._parser.add_section(section)

        self._parser.set(section, item, str(value))
