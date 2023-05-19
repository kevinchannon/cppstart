import unittest
from unittest.mock import MagicMock, call, patch
from datetime import datetime
from pathlib import Path

from cpp_start import *
from config import Config
from file_access import FileReadWriter
from file_info import FileInfo


class ArgParserTests(unittest.TestCase):
    def test_first_positional_argument_is_project_name(self):
        self.assertEqual("foo", get_command_line_parser([]).parse_args(["foo"]).proj_name)

    def test_output_directory_is_set_when_present(self):
        self.assertEqual("bar", get_command_line_parser([]).parse_args(["foo", "-o", "bar"]).output_directory)
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

    def test_build_system_is_set_when_present(self):
        self.assertEqual("meson",
                         get_command_line_parser([]).parse_args(["foo", "-b", "meson"]).build_system)
        self.assertEqual("meson",
                         get_command_line_parser([]).parse_args(["foo", "--build-system", "meson"]).build_system)

    def test_default_build_system_is_cmake(self):
        self.assertEqual("cmake", get_command_line_parser([""]).parse_args(["foo"]).build_system)

    def test_dependency_management_is_set_when_present(self):
        self.assertEqual("vcpkg",
                         get_command_line_parser([]).parse_args(["foo", "-d", "vcpkg"]).dependency_management)
        self.assertEqual("vcpkg",
                         get_command_line_parser([]).parse_args(
                             ["foo", "--dependency-management", "vcpkg"]).dependency_management)

    def test_default_dependency_management_is_conan(self):
        self.assertEqual("conan", get_command_line_parser([""]).parse_args(["foo"]).dependency_management)

    def test_source_control_is_set_when_present(self):
        self.assertEqual("mercurial",
                         get_command_line_parser([]).parse_args(["foo", "-s", "mercurial"]).source_control)
        self.assertEqual("mercurial",
                         get_command_line_parser([]).parse_args(
                             ["foo", "--source-control", "mercurial"]).source_control)

    def test_default_dependency_management_is_git(self):
        self.assertEqual("git", get_command_line_parser([""]).parse_args(["foo"]).source_control)

    def test_ci_is_set_when_present(self):
        with self.subTest("short arg"):
            self.assertEqual("jenkins",
                             get_command_line_parser([]).parse_args(["foo", "-i", "jenkins"]).ci)
        with self.subTest("long arg"):
            self.assertEqual("jenkins",
                             get_command_line_parser([]).parse_args(
                                 ["foo", "--ci", "jenkins"]).ci)

    def test_default_ci_is_github(self):
        self.assertEqual("github", get_command_line_parser([""]).parse_args(["foo"]).ci)


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

    def test_factory_write_the_expected_app_source_files(self):
        src_preamble = get_source_code_preamble("MIT", "2023", "Some Name")
        writer = FileReadWriter(Path("foo"))
        writer.write = MagicMock()

        args = get_command_line_parser([]).parse_args(["foo", "-c", "Some Name"])
        app = make_cppstart(args, self._empty_config)
        app.run(writer)

        write_calls = [
            call({FileInfo(Path("include/foo/foo.hpp"), f"{src_preamble}\n\n#include <cstdint>\n"),
                  FileInfo(Path(
                      "test/foo.tests.cpp"), f"{src_preamble}\n"
                                             f"\n"
                                             f"#include <foo/foo.hpp>\n"
                                             f"\n"
                                             f"#include <catch2/catch_test_macros.hpp>\n"
                                             f"\n"
                                             f"TEST_CASE(\"foo tests\") {{\n"
                                             f"    SECTION(\"delete this require and add your own tests!\")\n"
                                             f"        REQUIRE(false);\n"
                                             f"}}\n"),
                  FileInfo(Path("src/foo/foo.cpp"), f"{src_preamble}\n\n#include <foo/foo.hpp>\n"),
                  FileInfo(Path(
                      "src/main.cpp"),
                      f"{src_preamble}\n\n#include <foo/foo.hpp>\n\nauto main() -> int {{\n    return 0;\n}}\n")
                  }
                 )
        ]

        writer.write.assert_has_calls(write_calls)

    def test_factory_write_the_expected_lib_source_files(self):
        src_preamble = get_source_code_preamble("MIT", "2023", "Some Name")
        writer = FileReadWriter(Path("foo"))
        writer.write = MagicMock()

        args = get_command_line_parser([]).parse_args(["foo", "--lib", "-c", "Some Name"])
        app = make_cppstart(args, self._empty_config)
        app.run(writer)

        write_calls = [
            call({FileInfo(Path("include/foo/foo.hpp"), f"{src_preamble}\n\n#include <cstdint>\n"),
                  FileInfo(Path(
                      "examples/main.cpp"),
                      f"{src_preamble}\n\n#include <foo/foo.hpp>\n\nauto main() -> int {{\n    return 0;\n}}\n"),
                  FileInfo(Path(
                      "test/foo.tests.cpp"), f"{src_preamble}\n"
                                             f"\n"
                                             f"#include <foo/foo.hpp>\n"
                                             f"\n"
                                             f"#include <catch2/catch_test_macros.hpp>\n"
                                             f"\n"
                                             f"TEST_CASE(\"foo tests\") {{\n"
                                             f"    SECTION(\"delete this require and add your own tests!\")\n"
                                             f"        REQUIRE(false);\n"
                                             f"}}\n"),
                  FileInfo(Path("src/foo/foo.cpp"), f"{src_preamble}\n\n#include <foo/foo.hpp>\n")
                  }
                 )
        ]

        writer.write.assert_has_calls(write_calls)

    def test_writes_files(self):
        src_gen = AppSourceGenerator("foo")
        src_gen.run = MagicMock(return_value={FileInfo(Path("Some/Path"), "some content")})
        writer = FileReadWriter(Path("foo"))
        writer.write = MagicMock()

        build_sys_template_reader = FileReader(Path("build_sys_template/dir"))
        build_sys_template_reader.read_all = MagicMock(
            return_value={FileInfo(Path("build_sys_template/path"), "build sys template content")})
        build_sys_gen = Generator({}, build_sys_template_reader)

        deps_mgmt_template_reader = FileReader(Path("deps_mgmt_template/dir"))
        deps_mgmt_template_reader.read_all = MagicMock(
            return_value={FileInfo(Path("deps_mgmt_template/path"), "deps mgmt template content")})
        deps_mgmt_gen = Generator({}, deps_mgmt_template_reader)

        scm_template_reader = FileReader(Path("scm_template/dir"))
        scm_template_reader.read_all = MagicMock(
            return_value={FileInfo(Path("scm_template/path"), "scm template content")})
        scm_gen = Generator({}, scm_template_reader)

        ci_template_reader = FileReader(Path("ci_template/dir"))
        ci_template_reader.read_all = MagicMock(
            return_value={FileInfo(Path("ci_template/path"), "ci template content")})
        ci_gen = Generator({}, ci_template_reader)

        cpp_start = CppStart(source_generator=src_gen, build_system_generator=build_sys_gen,
                             deps_mgmt_generator=deps_mgmt_gen, scm_generator=scm_gen, ci_generator=ci_gen)
        cpp_start.run(writer)

        write_calls = [
            call({FileInfo(Path("Some/Path"), "some content")}),
            call({FileInfo(Path("build_sys_template/path"), "build sys template content")}),
            call({FileInfo(Path("deps_mgmt_template/path"), "deps mgmt template content")}),
            call({FileInfo(Path("scm_template/path"), "scm template content")}),
            call({FileInfo(Path("ci_template/path"), "ci template content")})
        ]

        writer.write.assert_has_calls(write_calls)
        self.assertTrue(build_sys_template_reader.read_all.called)
        self.assertTrue(deps_mgmt_template_reader.read_all.called)
        self.assertTrue(scm_template_reader.read_all.called)
        self.assertTrue(ci_template_reader.read_all.called)

    def test_get_config_doesnt_try_to_load_nonexistent_config(self):
        file_access = FileReadWriter(Path())
        file_access.exists = MagicMock(return_value=False)

        with patch.object(Config, "load") as mock_cfg_load:
            get_config(file_access)

        mock_cfg_load.assert_not_called()


class CopyrightNameTests(unittest.TestCase):
    class FakeArgs:
        def __init__(self, name):
            self.copyright_name = name

    def test_returns_value_from_args(self):
        self.assertEqual("Foo B Baz",
                         get_copyright_name(CopyrightNameTests.FakeArgs("Foo B Baz"), configparser.ConfigParser()))

    def test_gets_name_from_config_if_not_in_args(self):
        args = CopyrightNameTests.FakeArgs(None)

        file_access = FileReadWriter(Path())
        file_access.read = MagicMock(return_value="[user]\ncopyright_name@str = Name from config")

        config = Config(Path("config2.ini"), file_access)
        config.load()

        self.assertEqual("Name from config", get_copyright_name(args, config))

    @patch("cpp_start.input", create=True)
    def test_asks_for_copyright_name_if_not_in_args_or_config(self, fake_input_fn):
        fake_input_fn.side_effect = ["New User Name"]
        args = CopyrightNameTests.FakeArgs(None)
        file_access = FileReadWriter(Path())
        file_access.write = MagicMock()
        config = Config(Path("config3.ini"), file_access)

        self.assertEqual("New User Name", get_copyright_name(args, config))

    @patch("cpp_start.input", create=True)
    def test_writes_user_provided_copyright_name_to_config_if_not_in_args_or_config(self, fake_input_fn):
        fake_input_fn.side_effect = ["New User Name"]
        args = CopyrightNameTests.FakeArgs(None)
        file_access = FileReadWriter(Path())
        file_access.write = MagicMock()
        config = Config(Path("config4.ini"), file_access)

        _ = get_copyright_name(args, config)

        self.assertTrue(config.has("user", "copyright_name"))
        self.assertEqual("New User Name", config.get("user", "copyright_name"))
        file_access.write.assert_called_with({FileInfo(Path("config4.ini"), "[user]\ncopyright_name@str = New User Name\n\n")})


if __name__ == '__main__':
    unittest.main()
