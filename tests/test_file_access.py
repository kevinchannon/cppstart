import os
import unittest
from pathlib import Path
import shutil
from parameterized import parameterized

from src.cppstart.file_access import *


TEST_DIR = Path("test_files")


def get_many_files_in_hierarchy() -> dict[Path, str]:
    return {
        Path("a.txt"): "a.txt",
        Path("b.txt"): "b.txt",
        Path("c.txt"): "c.txt",
        Path("d/a.txt"): "da.txt",
        Path("d/b.txt"): "db.txt",
        Path("d/c.txt"): "dc.txt",
        Path("e/a.txt"): "ea.txt",
        Path("e/b.txt"): "eb.txt",
        Path("e/c.txt"): "ec.txt",
        Path("f/a.txt"): "fa.txt",
        Path("f/b.txt"): "fb.txt",
        Path("f/g/c.txt"): "fgc.txt",
        Path("h/i/a.txt"): "hia.txt",
        Path("h/i/b.txt"): "hib.txt",
        Path("h/i/c.txt"): "hic.txt",
        Path("h/i/j/a.txt"): "hija.txt",
        Path("h/i/j/b.txt"): "hijb.txt",
        Path("h/i/j/c.txt"): "hijc.txt",
        Path("h/i/j/k/l/m/c.txt"): "hijklmc.txt"
    }


class FileWriterTests(unittest.TestCase):
    def setup(self) -> None:
        os.makedirs(TEST_DIR, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(TEST_DIR, ignore_errors=True)
        if os.path.exists("foo.txt"):
            os.remove("foo.txt")

    @parameterized.expand([
        ("single file in current directory", Path("."), {Path("foo.txt"): "Hello, foo!"}),
        ("single file in a nested directory", TEST_DIR, {Path("foo/bar.txt"): "Hello, FooBar!"}),
        ("multiple files in multiple nested directories", TEST_DIR, get_many_files_in_hierarchy())
    ])
    def test_writes_contents_to_files(self, _, root_dir: Path, things_to_write: dict[Path, str]):
        writer = FileWriter(root_dir)
        writer.write(things_to_write)

        for rel_path in things_to_write:
            path = root_dir / rel_path
            self.assertTrue(path.exists())
            self.assertEqual(things_to_write[rel_path], path.read_text())


class FileReaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self._test_path = Path("test_file.txt")
        with open(self._test_path, "w") as f:
            print("hello!", file=f, end="")

    def tearDown(self) -> None:
        os.remove(self._test_path)

    def test_reads_file(self):
        reader = FileReader()
        self.assertEqual("hello!", reader.read(self._test_path))


if __name__ == '__main__':
    unittest.main()
