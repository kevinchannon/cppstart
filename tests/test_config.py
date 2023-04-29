import unittest
from unittest.mock import MagicMock

from src.cppstart.config import *


class ConfigTests(unittest.TestCase):
    _file_reader = FileReader()

    def setUp(self) -> None:
        self._file_reader.read = MagicMock(return_value="[user]\ncopyright_name = Person 123\n")

    def test_read_reads_the_config_file(self):
        config = Config(self._file_reader)
        config.read(Path("the/config/path.ini"))

        self._file_reader.read.assert_called_with(Path("the/config/path.ini"))
        self.assertEqual("Person 123", config.get("user", "copyright_name"))


if __name__ == '__main__':
    unittest.main()
