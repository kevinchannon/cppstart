import unittest
import sys
from pathlib import Path

from src.cppstart.source_builder import SourceBuilder


class SourceBuilderTests(unittest.TestCase):
    def test_adds_include_file(self):
        contents = SourceBuilder(Path("/foo")).get_content()
        self.assertTrue(Path("/foo/include/foo/foo.hpp") in contents)
        self.assertEqual(contents[Path("/foo/include/foo/foo.hpp")], "#include <cstdint>\n")

    def test_adds_example_files(self):
        contents = SourceBuilder(Path("/foo")).get_content()
        self.assertTrue(Path("/foo/examples/main.cpp") in contents)
        self.assertEqual(contents[Path("/foo/examples/main.cpp")],
                         "#include <proj_name/proj_name.hpp>\n\nauto main() -> int {\n    return 0;\n}\n")


if __name__ == '__main__':
    unittest.main()
