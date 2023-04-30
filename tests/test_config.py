import unittest
from unittest.mock import MagicMock
from parameterized import parameterized

from src.cppstart.config import *


class ConfigTests(unittest.TestCase):
    _file_reader = FileReader()

    def setUp(self) -> None:
        self._file_reader.read = MagicMock(return_value="[section1]\nsetting1@str = Person 123\n")

    def test_read_reads_the_config_file(self):
        config = Config(self._file_reader)
        config.read(Path("the/config/path.ini"))

        self._file_reader.read.assert_called_with(Path("the/config/path.ini"))
        self.assertEqual("Person 123", config.get("section1", "setting1"))

    def test_set_adds_new_section_and_value(self):
        config = Config(self._file_reader)
        config.set("section1", "setting1", 1000)

        self.assertEqual(1000, config.get("section1", "setting1"))

    @parameterized.expand([
        ("str", "Person 123"),
        ("int", 12345),
        ("float", 3.14152),
        ("bool", False),
        ("bool", True)
    ])
    def test_get_returns_value_with_type(self, item_type, value):
        self._file_reader.read = MagicMock(return_value=f"[section1]\nsetting1@{item_type} = {value}\n")
        config = Config(self._file_reader)
        config.read(Path("the/config/path.ini"))

        self.assertEqual(value, config.get("section1", "setting1"))

    @parameterized.expand([
        ("str", "Person 123"),
        ("int", 12345),
        ("float", 3.14152),
        ("bool", False),
        ("bool", True)
    ])
    def test_set_adds_value_with_type(self, _, value):
        config = Config(self._file_reader)
        config.set("section1", "setting1", value)

        self.assertEqual(value, config.get("section1", "setting1"))


if __name__ == '__main__':
    unittest.main()
