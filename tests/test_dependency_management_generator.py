import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized

from src.cppstart.dependency_management_generator import *


class CMakeGeneratorTests(unittest.TestCase):
    def test_reads_the_expected_template(self):
        template_files = {
            Path("conanfile.txt"): "[requires]\ncatch2/3.3.2\n\n[generators]\nbuild_sys_name\n",
            Path("other/file/path.txt"): "template\n\n\nproj_name textproj_name"
        }

        with patch.object(FileReader, "read_all", return_value=template_files) as fake_read_fn:
            generator = make_dependency_namagement_generator("conan", "cmake", Path("root"))
            contents = generator.run()

        self.assertEqual(Path("root/conan"), generator._template_reader.root_directory)

        expected_content = {
            Path("conanfile.txt"): "[requires]\ncatch2/3.3.2\n\n[generators]\ncmake\n",
            Path("other/file/path.txt"): "template\n\n\nproj_name textproj_name"
        }
        self.assertEqual(expected_content, contents)


if __name__ == '__main__':
    unittest.main()
