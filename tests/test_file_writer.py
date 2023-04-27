import os
import unittest
from pathlib import Path
import shutil
from parameterized import parameterized

from src.cppstart.file_writer import *


TEST_DIR = Path("test_files")


def get_many_files_in_hierarchy() -> dict[Path, str]:
    return {
        Path("foo.txt"): "foo.txt",
        TEST_DIR / "a.txt": "a.txt",
        TEST_DIR / "b.txt": "b.txt",
        TEST_DIR / "c.txt": "c.txt",
        TEST_DIR / "d/a.txt": "da.txt",
        TEST_DIR / "d/b.txt": "db.txt",
        TEST_DIR / "d/c.txt": "dc.txt",
        TEST_DIR / "e/a.txt": "ea.txt",
        TEST_DIR / "e/b.txt": "eb.txt",
        TEST_DIR / "e/c.txt": "ec.txt",
        TEST_DIR / "f/a.txt": "fa.txt",
        TEST_DIR / "f/b.txt": "fb.txt",
        TEST_DIR / "f/g/c.txt": "fgc.txt",
        TEST_DIR / "h/i/a.txt": "hia.txt",
        TEST_DIR / "h/i/b.txt": "hib.txt",
        TEST_DIR / "h/i/c.txt": "hic.txt",
        TEST_DIR / "h/i/j/a.txt": "hija.txt",
        TEST_DIR / "h/i/j/b.txt": "hijb.txt",
        TEST_DIR / "h/i/j/c.txt": "hijc.txt",
        TEST_DIR / "h/i/j/k/l/m/c.txt": "hijklmc.txt"
    }


class FileWriterTests(unittest.TestCase):
    def setup(self):
        os.makedirs(TEST_DIR, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(TEST_DIR, ignore_errors=True)
        if os.path.exists("foo.txt"):
            os.remove("foo.txt")

    @parameterized.expand([
        ("single file in current directory", {Path("foo.txt"): "Hello, foo!"}),
        ("single file in a nested directory", {TEST_DIR / "foo/bar.txt": "Hello, FooBar!"}),
        ("multiple files in multiple nested directories", get_many_files_in_hierarchy())
    ])
    def test_writes_contents_to_files(self, _, things_to_write):
        writer = FileWriter()
        writer.write(things_to_write)

        for path in things_to_write:
            self.assertTrue(path.exists())
            self.assertEqual(things_to_write[path], path.read_text())


if __name__ == '__main__':
    unittest.main()
