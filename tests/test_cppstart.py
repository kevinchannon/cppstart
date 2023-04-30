import unittest
from unittest.mock import MagicMock, call
from datetime import datetime
from pathlib import Path
import configparser

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

    def test_copyright_name_is_correct_if_present(self):
        self.assertEqual("The Copyright Name",
                         get_command_line_parser().parse_args(["foo", "-c", "The Copyright Name"]).copyright_name)
        self.assertEqual("The Copyright Name", get_command_line_parser().parse_args(
            ["foo", "--copyright-name", "The Copyright Name"]).copyright_name)


class CppStartTests(unittest.TestCase):

    def test_factory_creates_lib_source_builder_when_args_has_is_lib(self):
        args = get_command_line_parser().parse_args(["foo", "--lib"])
        app = make_cppstart(args, None)
        self.assertTrue(isinstance(app._source_generator, LibSourceGenerator))

    def test_factory_creates_app_source_builder_when_args_has_is_app(self):
        args = get_command_line_parser().parse_args(["foo", "--app"])
        app = make_cppstart(args, None)
        self.assertTrue(isinstance(app._source_generator, AppSourceGenerator))

    def test_factory_write_the_expected_source_files(self):
        src_preamble = get_source_code_preamble("MIT", str(datetime.now().year), "Some Name")
        writer = FileReadWriter(Path("foo"))
        writer.write = MagicMock()

        args = get_command_line_parser().parse_args(["foo", "-c", "Some Name"])
        app = make_cppstart(args, None)
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
        writer = FileReadWriter(Path("foo"))
        writer.write = MagicMock()

        cpp_start = CppStart(source_generator=src_gen)
        cpp_start.run(writer)

        writer.write.assert_called_with({Path("Some/Path"): "some content"})


class CopyrightNameTests(unittest.TestCase):
    class FakeArgs:
        copyright_name = "Foo B Baz"

    def test_returns_value_from_args(self):
        self.assertEqual("Foo B Baz", get_copyright_name(CopyrightNameTests.FakeArgs(), configparser.ConfigParser()))

    @unittest.skip("Need to implement Config first")
    def test_gets_name_from_config_if_not_in_args(self):
        args = CopyrightNameTests.FakeArgs()
        args.copyright_name = None

        config = configparser.ConfigParser()
        config["user"] = {"copyright_name": "Name from config"}
        self.assertEqual("Name from config", get_copyright_name(args, config))


if __name__ == '__main__':
    unittest.main()
