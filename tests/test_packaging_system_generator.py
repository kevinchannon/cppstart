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
