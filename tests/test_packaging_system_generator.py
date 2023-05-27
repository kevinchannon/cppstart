import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized

from packaging_system_generator import *
from file_info import FileInfo


class ConanGeneratorTests(unittest.TestCase):
    def test_reads_the_expected_template(self):
        template_files = {
            FileInfo(Path("dir/file.txt"),
                     "template proj_name textproj_name\n"
                     "\n"
                     "license = \"$license_name\"\n"
                     "author = \"$copyright_name $author_email\"\n"
                     "url = \"$url\"")
        }

        with patch.object(FileReader, "read_all", return_value=template_files) as fake_read_fn:
            generator = make_packaging_system_generator("some_packaging_sys", "foo", "MIT", "Some copyright name",
                                                        "me@there.com", "https://github.com/githubuser/foo",
                                                        Path("root"))
            files = generator.run()

        self.assertEqual(Path("root/some_packaging_sys"), generator._template_reader.root_directory)

        self.assertEqual(1, len(files))

        expected_content = "template foo textfoo\n" \
                           "\n" \
                           "license = \"MIT\"\n" \
                           "author = \"Some copyright name me@there.com\"\n" \
                           "url = \"https://github.com/githubuser/foo\""

        self.assertIn(FileInfo(Path("dir/file.txt"), expected_content), files)

    def test_renames_conan_files_marked_for_renaming(self):
        template_files = {
            FileInfo(Path("dir/file1.rename_to_py"), "File 1 content"),
            FileInfo(Path("dir/file2.txt"), "File 2 content"),
            FileInfo(Path("dir/file3.rename_to_py"), "File 3 content")
        }

        with patch.object(FileReader, "read_all", return_value=template_files) as fake_read_fn:
            generator = make_packaging_system_generator("conan", "foo", "MIT", "Some copyright name",
                                                        "me@there.com", "https://github.com/githubuser/foo",
                                                        Path("root"))
            files = generator.run()

        self.assertEqual(3, len(files))

        self.assertIn(FileInfo(Path("dir/file1.py"), "File 1 content"), files)
        self.assertIn(FileInfo(Path("dir/file2.txt"), "File 2 content"), files)
        self.assertIn(FileInfo(Path("dir/file3.py"), "File 3 content"), files)
