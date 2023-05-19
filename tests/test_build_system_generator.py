import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized

from build_system_generator import *
from file_info import FileInfo
from project_type import ProjectType


class CMakeGeneratorTests(unittest.TestCase):
    def test_reads_the_expected_template(self):
        template_files = {
            FileInfo(Path("dir/file.txt"), "template proj_name textproj_name"),
            FileInfo(Path("file.txt"), "template\n\n\nproj_name textproj_name")
        }

        with patch.object(FileReader, "read_all", return_value=template_files) as fake_read_fn:
            generator = make_build_system_generator("some_build_sys", "foo", ProjectType.LIB, Path("root"))
            contents = generator.run()

        self.assertEqual(Path("root/some_build_sys"), generator._template_reader.root_directory)

        expected_content = {
            FileInfo(Path("dir/file.txt"), "template foo textfoo"),
            FileInfo(Path("file.txt"), "template\n\n\nfoo textfoo")
        }

        for expected in expected_content:
            contents.remove(expected)

        self.assertTrue(len(contents) == 0)

    def test_factory_returns_cmake_generator_if_requested(self):
        generator = make_build_system_generator("cmake", "foo", ProjectType.LIB, Path("root"))
        self.assertIsInstance(generator, CMakeGenerator)

    def test_cmake_generator_removes_main_cpp_file(self):
        template_files = {
            FileInfo(Path("src/CMakeLists.txt"), "cmake_minimum_required(VERSION 3.15)\n\nadd_executable(proj_name\n  "
                                                 "main.cpp\n)\ninclude(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)"),
            FileInfo(Path("examples/CMakeLists.txt"),
                     "cmake_minimum_required(VERSION 3.15)\n\nadd_executable(proj_name\n  "
                     "main.cpp\n)\ninclude(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)")
        }

        with patch.object(FileReader, "read_all", return_value=template_files) as fake_read_fn:
            generator = make_build_system_generator("cmake", "foo", ProjectType.LIB, Path("root"))
            contents = generator.run()

        expected_content = {
            FileInfo(Path("src/CMakeLists.txt"), "cmake_minimum_required(VERSION 3.15)\n\ninclude(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)"),
            FileInfo(Path("examples/CMakeLists.txt"),
                     "cmake_minimum_required(VERSION 3.15)\n\nadd_executable(foo\n  "
                     "main.cpp\n)\ninclude(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)")
        }

        for expected in expected_content:
            contents.remove(expected)

        self.assertTrue(len(contents) == 0)


if __name__ == '__main__':
    unittest.main()
