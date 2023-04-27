import os
import unittest
from pathlib import Path

from src.cppstart.file_writer import *


class FileWriterTests(unittest.TestCase):
    _file_in_current_dir = Path("foo.txt")

    def tearDown(self):
        if self._file_in_current_dir.exists():
            os.remove(self._file_in_current_dir)

    def test_writes_contents_to_files_in_current_directory(self):
        writer = FileWriter()
        writer.write({self._file_in_current_dir: "Hello, Foo!"})

        self.assertTrue(self._file_in_current_dir.exists())
        self.assertEqual("Hello, Foo!", self._file_in_current_dir.read_text())


if __name__ == '__main__':
    unittest.main()
