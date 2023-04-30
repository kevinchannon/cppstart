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
        getters = {"str": self._parser.get,
                   "int": self._parser.getint,
                   "float": self._parser.getfloat,
                   "bool": self._parser.getboolean}

        for t in getters:
            typed_item = f"{item}@{t}"
            if self._parser.has_option(section, typed_item):
                return getters[t](section, typed_item)

    def set(self, section: str, item: str, value):
        if not self._parser.has_section(section):
            self._parser.add_section(section)

        if isinstance(value, bool):
            self._parser.set(section, f"{item}@bool", str(value))
        elif isinstance(value, int):
            self._parser.set(section, f"{item}@int", str(value))
        elif isinstance(value, float):
            self._parser.set(section, f"{item}@float", str(value))
        else:
            self._parser.set(section, f"{item}@str", str(value))
