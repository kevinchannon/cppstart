import unittest
from unittest.mock import MagicMock, call
from datetime import datetime
from pathlib import Path

from src.cppstart.cppstart import *


class ArgParserTests(unittest.TestCase):
    def test_first_positional_argument_is_project_name(self):
        self.assertEqual("foo", get_command_line_parser().parse_args(["foo"]).proj_name)

    def test_output_directory_is_set_when_present(self):
        self.assertEqual("bar", get_command_line_parser().parse_args(["foo", "-d", "bar"]).output_directory)
        self.assertEqual("bar",
                         get_command_line_parser().parse_args(["foo", "--output-directory", "bar"]).output_directory)

    def test_output_directory_is_set_to_dot_when_absent(self):
        self.assertEqual(".", get_command_line_parser().parse_args(["foo"]).output_directory)

    def test_project_type_is_set_correctly(self):
        self.assertEqual(ProjectType.LIB, get_command_line_parser().parse_args(["foo", "--lib"]).project_type)
        self.assertEqual(ProjectType.LIB, get_command_line_parser().parse_args(["foo", "-L"]).project_type)

        self.assertEqual(ProjectType.APP, get_command_line_parser().parse_args(["foo", "--app"]).project_type)
        self.assertEqual(ProjectType.APP, get_command_line_parser().parse_args(["foo", "-A"]).project_type)

    def test_default_project_type_is_app(self):
        self.assertEqual(ProjectType.APP, get_command_line_parser().parse_args(["foo"]).project_type)

    def test_license_is_set_when_present(self):
        self.assertEqual("MIT", get_command_line_parser().parse_args(["foo", "-l", "MIT"]).license)
        self.assertEqual("MIT", get_command_line_parser().parse_args(["foo", "--license=MIT"]).license)

    def test_default_license_is_MIT(self):
        self.assertEqual("MIT", get_command_line_parser().parse_args(["foo"]).license)


class CppStartTests(unittest.TestCase):
    def test_factory_creates_lib_source_builder_when_args_has_is_lib(self):
        args = get_command_line_parser().parse_args(["foo", "--lib"])
        app = make_cppstart(args)
        self.assertTrue(isinstance(app._source_generator, LibSourceGenerator))

    def test_factory_creates_app_source_builder_when_args_has_is_app(self):
        args = get_command_line_parser().parse_args(["foo", "--app"])
        app = make_cppstart(args)
        self.assertTrue(isinstance(app._source_generator, AppSourceGenerator))

    def test_factory_write_the_expected_source_files(self):
        src_preamble = get_source_code_preamble("MIT", str(datetime.now().year), "Some Name")
        writer = FileWriter(Path("foo"))
        writer.write = MagicMock()

        args = get_command_line_parser().parse_args(["foo"])
        app = make_cppstart(args)
        app.run(writer)

        write_calls = [
            call({Path("include/foo/foo.hpp"): f"{src_preamble}\n\n#include <cstdint>\n",
                  Path(
                      "examples/main.cpp"): f"{src_preamble}\n\n#include <proj_name/proj_name.hpp>\n\nauto main() -> int {{\n    return 0;\n}}\n",
                  Path("src/foo/foo.cpp"): f"{src_preamble}\n\n#include <proj_name/proj_name.hpp>\n",
                  Path(
                      "src/main.cpp"): f"{src_preamble}\n\n#include <proj_name/proj_name.hpp>\n\nauto main() -> int {{\n    return 0;\n}}\n"}
                 )
        ]

        writer.write.assert_has_calls(write_calls)

    def test_writes_files(self):
        src_gen = AppSourceGenerator("foo")
        src_gen.run = MagicMock(return_value={Path("Some/Path"): "some content"})
        writer = FileWriter(Path("foo"))
        writer.write = MagicMock()

        cpp_start = CppStart(source_generator=src_gen)
        cpp_start.run(writer)

        writer.write.assert_called_with({Path("Some/Path"): "some content"})


if __name__ == '__main__':
    unittest.main()
