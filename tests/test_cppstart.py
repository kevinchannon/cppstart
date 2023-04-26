import unittest

from src.cppstart.cppstart import *


class ArgParserTests(unittest.TestCase):
    def test_first_positional_argument_is_project_name(self):
        self.assertEqual("foo", get_command_line_parser().parse_args(["foo"]).proj_name)


if __name__ == '__main__':
    unittest.main()
