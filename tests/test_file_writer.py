import os
import unittest
from pathlib import Path
import shutil
from parameterized import parameterized

from src.cppstart.file_writer import *


TEST_DIR = Path("test_files")


class FileWriterTests(unittest.TestCase):
    def setup(self):
        os.makedirs(TEST_DIR, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(TEST_DIR, ignore_errors=True)
        if os.path.exists("foo.txt"):
            os.remove("foo.txt")

    @parameterized.expand([
        ("single file in current directory", {Path("foo.txt"): "Hello, foo!"}),
        ("single file in a nested directory", {TEST_DIR / "foo/bar.txt": "Hello, FooBar!"})
    ])
    def test_writes_contents_to_files(self, test_name, things_to_write):
        writer = FileWriter()
        writer.write(things_to_write)

        for path in things_to_write:
            self.assertTrue(path.exists())
            self.assertEqual(things_to_write[path], path.read_text())


if __name__ == '__main__':
    unittest.main()
