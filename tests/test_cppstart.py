import unittest
from unittest.mock import MagicMock, call, patch
from datetime import datetime
from pathlib import Path

from src.cppstart.cppstart import *
from src.cppstart.config import Config
from src.cppstart.file_access import FileReadWriter


class ArgParserTests(unittest.TestCase):
    def test_first_positional_argument_is_project_name(self):
        self.assertEqual("foo", get_command_line_parser([]).parse_args(["foo"]).proj_name)

    def test_output_directory_is_set_when_present(self):
        self.assertEqual("bar", get_command_line_parser([]).parse_args(["foo", "-d", "bar"]).output_directory)
        self.assertEqual("bar",
                         get_command_line_parser([]).parse_args(["foo", "--output-directory", "bar"]).output_directory)

    def test_output_directory_is_set_to_dot_when_absent(self):
        self.assertEqual(".", get_command_line_parser([]).parse_args(["foo"]).output_directory)

    def test_project_type_is_set_correctly(self):
        self.assertEqual(ProjectType.LIB, get_command_line_parser([]).parse_args(["foo", "--lib"]).project_type)
        self.assertEqual(ProjectType.LIB, get_command_line_parser([]).parse_args(["foo", "-L"]).project_type)

        self.assertEqual(ProjectType.APP, get_command_line_parser([]).parse_args(["foo", "--app"]).project_type)
        self.assertEqual(ProjectType.APP, get_command_line_parser([]).parse_args(["foo", "-A"]).project_type)

    def test_default_project_type_is_app(self):
        self.assertEqual(ProjectType.APP, get_command_line_parser([]).parse_args(["foo"]).project_type)

    def test_license_is_set_when_present(self):
        self.assertEqual("MIT", get_command_line_parser(["MIT"]).parse_args(["foo", "-l", "MIT"]).license)
        self.assertEqual("MIT", get_command_line_parser(["MIT"]).parse_args(["foo", "--license=MIT"]).license)

    def test_default_license_is_MIT(self):
        self.assertEqual("MIT", get_command_line_parser(["MIT"]).parse_args(["foo"]).license)

    def test_copyright_name_is_correct_if_present(self):
        self.assertEqual("The Copyright Name",
                         get_command_line_parser([]).parse_args(["foo", "-c", "The Copyright Name"]).copyright_name)
        self.assertEqual("The Copyright Name", get_command_line_parser([]).parse_args(
            ["foo", "--copyright-name", "The Copyright Name"]).copyright_name)


class CppStartTests(unittest.TestCase):
    _empty_config = Config(Path(), FileReadWriter(Path()))

    def test_factory_creates_lib_source_builder_when_args_has_is_lib(self):
        args = get_command_line_parser([]).parse_args(["foo", "--lib", "-c", "bar"])
        app = make_cppstart(args, self._empty_config)
        self.assertTrue(isinstance(app._source_generator, LibSourceGenerator))

    def test_factory_creates_app_source_builder_when_args_has_is_app(self):
        args = get_command_line_parser([]).parse_args(["foo", "--app", "-c", "bar"])
        app = make_cppstart(args, self._empty_config)
        self.assertTrue(isinstance(app._source_generator, AppSourceGenerator))

    def test_factory_write_the_expected_source_files(self):
        src_preamble = get_source_code_preamble("MIT", str(datetime.now().year), "Some Name")
        writer = FileReadWriter(Path("foo"))
        writer.write = MagicMock()

        args = get_command_line_parser([]).parse_args(["foo", "-c", "Some Name"])
        app = make_cppstart(args, self._empty_config)
        app.run(writer)

        write_calls = [
            call({Path("include/foo/foo.hpp"): f"{src_preamble}\n\n#include <cstdint>\n",
                  Path(
                      "examples/main.cpp"): f"{src_preamble}\n\n#include <foo/foo.hpp>\n\nauto main() -> int {{\n    return 0;\n}}\n",
                  Path("src/foo/foo.cpp"): f"{src_preamble}\n\n#include <foo/foo.hpp>\n",
                  Path(
                      "src/main.cpp"): f"{src_preamble}\n\n#include <foo/foo.hpp>\n\nauto main() -> int {{\n    return 0;\n}}\n"}
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
        def __init__(self, name):
            self.copyright_name = name

    def test_returns_value_from_args(self):
        self.assertEqual("Foo B Baz", get_copyright_name(CopyrightNameTests.FakeArgs("Foo B Baz"), configparser.ConfigParser()))

    def test_gets_name_from_config_if_not_in_args(self):
        args = CopyrightNameTests.FakeArgs(None)

        file_access = FileReadWriter(Path())
        file_access.read = MagicMock(return_value="[user]\ncopyright_name@str = Name from config")

        config = Config(Path("config.ini"), file_access)
        config.load()

        self.assertEqual("Name from config", get_copyright_name(args, config))

    @patch("src.cppstart.cppstart.input", create=True)
    def test_asks_for_copyright_name_if_not_in_args_or_config(self, fake_input_fn):
        fake_input_fn.side_effect = ["New User Name"]
        args = CopyrightNameTests.FakeArgs(None)
        file_access = FileReadWriter(Path())
        config = Config(Path("config.ini"), file_access)

        self.assertEqual("New User Name", get_copyright_name(args, config))

    @patch("src.cppstart.cppstart.input", create=True)
    def test_writes_user_provided_copyright_name_to_config_if_not_in_args_or_config(self, fake_input_fn):
        fake_input_fn.side_effect = ["New User Name"]
        args = CopyrightNameTests.FakeArgs(None)
        file_access = FileReadWriter(Path())
        file_access.write = MagicMock()
        config = Config(Path("config.ini"), file_access)

        _ = get_copyright_name(args, config)

        self.assertTrue(config.has("user", "copyright_name"))
        self.assertEqual("New User Name", config.get("user", "copyright_name"))
        file_access.write.assert_called_with({Path("config.ini"): "[user]\ncopyright_name@str = New User Name\n\n"})


if __name__ == '__main__':
    unittest.main()
