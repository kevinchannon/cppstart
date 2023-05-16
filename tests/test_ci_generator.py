import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized

from ci_generator import *
from file_info import FileInfo


class GithubWorkflowsGeneratorTests(unittest.TestCase):
    def test_reads_the_expected_template(self):
        template_files = {
            FileInfo(Path("dir/file.txt"), "template proj_name textproj_name"),
            FileInfo(Path("file.txt"), "template\n\n\nproj_name textproj_name")
        }

        with patch.object(FileReader, "read_all", return_value=template_files) as fake_read_fn:
            generator = make_ci_generator("github", "foo", Path("root"))
            contents = generator.run()

        self.assertEqual(Path("root/github"), generator._template_reader.root_directory)

        expected_content = {
            FileInfo(Path("dir/file.txt"), "template foo textfoo"),
            FileInfo(Path("file.txt"), "template\n\n\nfoo textfoo")
        }

        self.assertTrue(expected_content == contents)


if __name__ == '__main__':
    unittest.main()
