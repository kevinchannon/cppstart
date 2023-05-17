import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized

from dependency_management_generator import *
from file_info import FileInfo


class ConanGeneratorTests(unittest.TestCase):
    def test_reads_the_expected_template(self):
        template_files = {
            FileInfo(Path("conanfile.txt"), "[requires]\ncatch2/3.3.2\n\n[generators]\nbuild_sys_name\n"),
            FileInfo(Path("other/file/path.txt"), "template\n\n\nproj_name textproj_name")
        }

        with patch.object(FileReader, "read_all", return_value=template_files) as fake_read_fn:
            generator = make_dependency_namagement_generator("conan", "cmake", Path("root"))
            contents = generator.run()

        self.assertEqual(Path("root/conan"), generator._template_reader.root_directory)

        expected_content = {
            FileInfo(Path("conanfile.txt"), "[requires]\ncatch2/3.3.2\n\n[generators]\ncmake\n"),
            FileInfo(Path("other/file/path.txt"), "template\n\n\nproj_name textproj_name")
        }

        for expected in expected_content:
            contents.remove(expected)

        self.assertTrue(len(contents) == 0)

    def test_init_files_are_executable(self):
        template_files = {
            FileInfo(Path("file.txt"), "content", 0o644),
            FileInfo(Path("init.sh"), "init", 0o644),
            FileInfo(Path("init.ps1"), "init", 0o644)
        }

        with patch.object(FileReader, "read_all", return_value=template_files) as fake_read_fn:
            generator = make_dependency_namagement_generator("conan", "cmake", Path("root"))
            files = generator.run()

        for name, path in [("bash script", Path("init.sh")), ("powershell script", Path("init.ps1"))]:
            with self.subTest(name):
                script = next((f for f in files if f.path == path), None)
                self.assertIsNotNone(script)
                self.assertEqual(0o755, script.permissions)


if __name__ == '__main__':
    unittest.main()
