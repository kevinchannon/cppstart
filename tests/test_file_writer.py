import os
import unittest
from pathlib import Path
from parameterized import parameterized

from src.cppstart.file_writer import *


class FileWriterTests(unittest.TestCase):
    _things_to_remove = []

    def tearDown(self):
        for path in self._things_to_remove:
            os.remove(path)

    @parameterized.expand([
        ("single file in current directory", {Path("foo.txt"): "Hello, foo!"})
    ])
    def test_writes_contents_to_files(self, test_name, things_to_write):
        writer = FileWriter()
        writer.write(things_to_write)

        for path in things_to_write:
            self.assertTrue(path.exists())
            self._things_to_remove.append(path)
            self.assertEqual(things_to_write[path], path.read_text())


if __name__ == '__main__':
    unittest.main()
