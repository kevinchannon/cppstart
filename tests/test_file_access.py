import os
import unittest
from unittest.mock import patch
from pathlib import Path
import shutil
from parameterized import parameterized

from file_access import *
from src.cppstart import file_info


TEST_DIR = Path("test_files")


def get_many_files_in_hierarchy() -> set[FileInfo]:
    return {
        FileInfo(Path("a.txt"), "a.txt"),
        FileInfo(Path("b.txt"), "b.txt"),
        FileInfo(Path("c.txt"), "c.txt"),
        FileInfo(Path("d/a.txt"), "da.txt"),
        FileInfo(Path("d/b.txt"), "db.txt"),
        FileInfo(Path("d/c.txt"), "dc.txt"),
        FileInfo(Path("e/a.txt"), "ea.txt"),
        FileInfo(Path("e/b.txt"), "eb.txt"),
        FileInfo(Path("e/c.txt"), "ec.txt"),
        FileInfo(Path("f/a.txt"), "fa.txt"),
        FileInfo(Path("f/b.txt"), "fb.txt"),
        FileInfo(Path("f/g/c.txt"), "fgc.txt"),
        FileInfo(Path("h/i/a.txt"), "hia.txt"),
        FileInfo(Path("h/i/b.txt"), "hib.txt"),
        FileInfo(Path("h/i/c.txt"), "hic.txt"),
        FileInfo(Path("h/i/j/a.txt"), "hija.txt"),
        FileInfo(Path("h/i/j/b.txt"), "hijb.txt"),
        FileInfo(Path("h/i/j/c.txt"), "hijc.txt"),
        FileInfo(Path("h/i/j/k/l/m/c.txt"), "hijklmc.txt")
    }


def make_files_in_hierarchy(files: set[FileInfo]):
    for file in files:
        directory = TEST_DIR / file.path.parent
        if not directory.exists():
            os.makedirs(directory)

        with open(TEST_DIR / file.path, "w") as f:
            f.write(file.content)


class FileWriterTests(unittest.TestCase):
    def setup(self) -> None:
        os.makedirs(TEST_DIR, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(TEST_DIR, ignore_errors=True)
        if os.path.exists("foo.txt"):
            os.remove("foo.txt")

    @parameterized.expand([
        ("single file in current directory", Path("."), {FileInfo(Path("foo.txt"), "Hello, foo!")}),
        ("single file in a nested directory", TEST_DIR, {FileInfo(Path("foo/bar.txt"), "Hello, FooBar!")}),
        ("multiple files in multiple nested directories", TEST_DIR, get_many_files_in_hierarchy())
    ])
    def test_writes_contents_to_files(self, _, root_dir: Path, things_to_write: set[FileInfo]):
        writer = FileReadWriter(root_dir)
        writer.write(things_to_write)

        for info in things_to_write:
            path = root_dir / info.path
            self.assertTrue(path.exists())
            self.assertEqual(info.content, path.read_text())


class FileReaderTests(unittest.TestCase):
    def setUp(self) -> None:
        self._test_path = Path("test_file.txt")

    def tearDown(self) -> None:
        if self._test_path.exists():
            self._test_path.unlink()

        shutil.rmtree(TEST_DIR, ignore_errors=True)

    def test_reads_file(self):
        self._test_path = Path("test_file.txt")
        with open(self._test_path, "w") as f:
            print("hello!", file=f, end="")

        reader = FileReader()
        self.assertEqual("hello!", reader.read(self._test_path))

    def test_reads_files_in_root_directory(self):
        os.makedirs(TEST_DIR, exist_ok=True)
        with open(TEST_DIR / self._test_path, "w") as f:
            print("hello, sub-dir!", file=f, end="")

        reader = FileReader(TEST_DIR)
        self.assertEqual("hello, sub-dir!", reader.read(self._test_path))

    def test_exists_returns_false_if_path_doesnt_exist(self):
        reader = FileReader(Path())
        with patch.object(Path, "exists", return_value=False):
            self.assertFalse(reader.exists(Path("not_a_path.txt")))

    def test_read_all_reads_all_the_files_in_the_directory(self):
        make_files_in_hierarchy(get_many_files_in_hierarchy())

        reader = FileReader(TEST_DIR)
        self.assertEqual(get_many_files_in_hierarchy(), reader.read_all())


if __name__ == '__main__':
    unittest.main()
