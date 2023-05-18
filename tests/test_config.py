import unittest
from unittest.mock import MagicMock
from parameterized import parameterized

from config import *
from file_access import *


class ConfigTests(unittest.TestCase):
    _file_access = FileReadWriter(Path("config/dir"))

    def setUp(self) -> None:
        self._file_access.read = MagicMock(return_value="[section1]\nsetting1@str = Person 123\n")

    def test_load_reads_the_config_file(self):
        config = Config(Path("cfg.ini"), self._file_access)
        config.load()

        self._file_access.read.assert_called_with(Path("cfg.ini"))
        self.assertEqual("Person 123", config.get("section1", "setting1"))

    def test_save_writes_the_config_file(self):
        config = Config(Path("cfg.ini"), self._file_access)
        config.set("section1", "setting1", "value1")
        config.set("section1", "setting2", 1000)
        config.set("section1", "setting3", 2.7)
        config.set("section1", "setting4", False)
        config.set("section2", "setting1", "value2")
        config.set("section2", "setting2", 2000)
        config.set("section2", "setting3", 1.618)
        config.set("section2", "setting4", True)

        self._file_access.write = MagicMock()

        config.save()

        self._file_access.write.assert_called_with({FileInfo(Path(
            "cfg.ini"), "[section1]\n"
                        "setting1@str = value1\n"
                        "setting2@int = 1000\n"
                        "setting3@float = 2.7\n"
                        "setting4@bool = False\n"
                        "\n"
                        "[section2]\n"
                        "setting1@str = value2\n"
                        "setting2@int = 2000\n"
                        "setting3@float = 1.618\n"
                        "setting4@bool = True\n"
                        "\n")})

    def test_set_adds_new_section_and_value(self):
        config = Config(Path("cfg.ini"), self._file_access)
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
        self._file_access.read = MagicMock(return_value=f"[section1]\nsetting1@{item_type} = {value}\n")
        config = Config(Path("cfg.ini"), self._file_access)
        config.load()

        self.assertEqual(value, config.get("section1", "setting1"))

    @parameterized.expand([
        ("str", "Person 123"),
        ("int", 12345),
        ("float", 3.14152),
        ("bool", False),
        ("bool", True)
    ])
    def test_set_adds_value_with_type(self, _, value):
        config = Config(Path("cfg.ini"), self._file_access)
        config.set("section1", "setting1", value)

        self.assertEqual(value, config.get("section1", "setting1"))

    @parameterized.expand([
        ("str", "Person 123"),
        ("int", 12345),
        ("float", 3.14152),
        ("bool", False),
        ("bool", True)
    ])
    def test_has_returns_true_if_the_value_is_present(self, _, value):
        config = Config(Path("cfg.ini"), self._file_access)
        config.set("section1", "setting1", value)

        self.assertTrue(config.has("section1", "setting1"))

    def test_has_returns_false_if_the_value_is_not_present(self):
        config = Config(Path("cfg.ini"), self._file_access)
        config.set("section1", "setting1", 1000)

        self.assertFalse(config.has("section1", "setting2"))

    def test_has_returns_false_if_the_section_is_not_present(self):
        config = Config(Path("cfg.ini"), self._file_access)
        config.set("section1", "setting1", 1000)

        self.assertFalse(config.has("section2", "setting1"))


if __name__ == '__main__':
    unittest.main()
