import configparser
from pathlib import Path
from io import StringIO

from file_access import FileReadWriter
from file_info import FileInfo


class Config:
    def __init__(self, filename: Path, file_access: FileReadWriter):
        self._parser = configparser.ConfigParser()
        self._filename = filename
        self._file_access = file_access

    def load(self):
        config_str = self._file_access.read(self._filename)
        self._parser.read_string(config_str)

    def save(self):
        with StringIO() as cfg_str:
            self._parser.write(cfg_str)
            cfg_str.seek(0)

            self._file_access.write({FileInfo(self._filename, cfg_str.read())})

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

    def has(self, section: str, item: str) -> bool:
        types = ["str", "int", "float", "bool"]

        if self._parser.has_section(section):
            for t in types:
                typed_item = f"{item}@{t}"
                if self._parser.has_option(section, typed_item):
                    return True

        return False
