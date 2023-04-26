import unittest

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
        self.assertTrue(get_command_line_parser().parse_args(["foo", "--lib"]).is_lib)
        self.assertFalse(get_command_line_parser().parse_args(["foo", "--lib"]).is_app)
        self.assertTrue(get_command_line_parser().parse_args(["foo", "-L"]).is_lib)
        self.assertFalse(get_command_line_parser().parse_args(["foo", "-L"]).is_app)

        self.assertFalse(get_command_line_parser().parse_args(["foo", "--app"]).is_lib)
        self.assertTrue(get_command_line_parser().parse_args(["foo", "--app"]).is_app)
        self.assertFalse(get_command_line_parser().parse_args(["foo", "-A"]).is_lib)
        self.assertTrue(get_command_line_parser().parse_args(["foo", "-A"]).is_app)


if __name__ == '__main__':
    unittest.main()
