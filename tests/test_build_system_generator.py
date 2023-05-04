import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized

from src.cppstart.build_system_generator import *


class CMakeGeneratorTests(unittest.TestCase):
    def test_reads_the_expected_template(self):
        template_files = {
            Path("dir/file.txt"): "template proj_name textproj_name",
            Path("file.txt"): "template\n\n\nproj_name textproj_name"
        }

        with patch.object(FileReader, "read_all", return_value=template_files) as fake_read_fn:
            generator = make_build_system_generator("cmake", "foo", Path("root"))
            contents = generator.run()

        self.assertEqual(Path("root/cmake"), generator._template_reader.root_directory)

        expected_content = {
            Path("dir/file.txt"): "template foo textfoo",
            Path("file.txt"): "template\n\n\nfoo textfoo"
        }
        self.assertEqual(expected_content, contents)


if __name__ == '__main__':
    unittest.main()
