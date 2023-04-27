import unittest
from parameterized import parameterized
from pathlib import Path

from src.cppstart.source_builder import *


class SourceBuilderTests(unittest.TestCase):
    @parameterized.expand([
        AppSourceBuilder("foo"),
        LibSourceBuilder("foo")
    ])
    def test_adds_include_file(self, builder):
        contents = builder.get_content()
        self.assertTrue(Path("include/foo/foo.hpp") in contents)
        self.assertEqual(contents[Path("include/foo/foo.hpp")], "#include <cstdint>\n")

    @parameterized.expand([
        AppSourceBuilder("foo"),
        LibSourceBuilder("foo")
    ])
    def test_adds_example_files(self, builder):
        contents = builder.get_content()
        self.assertTrue(Path("examples/main.cpp") in contents)
        self.assertEqual(contents[Path("examples/main.cpp")],
                         "#include <proj_name/proj_name.hpp>\n\nauto main() -> int {\n    return 0;\n}\n")

    @parameterized.expand([
        AppSourceBuilder("foo"),
        LibSourceBuilder("foo")
    ])
    def test_adds_source_files(self, builder):
        contents = builder.get_content()
        self.assertTrue(Path("src/foo/foo.cpp") in contents)
        self.assertEqual(contents[Path("src/foo/foo.cpp")], "#include <proj_name/proj_name.hpp>\n")

    def test_app_source_builder_adds_main(self):
        contents = AppSourceBuilder("foo").get_content()
        self.assertTrue(Path("src/main.cpp") in contents)
        self.assertEqual(contents[Path("src/main.cpp")],
                         "#include <proj_name/proj_name.hpp>\n\nauto main() -> int {\n    return 0;\n}\n")

    def test_lib_source_builder_does_not_add_main(self):
        contents = LibSourceBuilder("foo").get_content()
        self.assertFalse(Path("src/main.cpp") in contents)

    def test_source_builder_factory_returns_an_app_builder(self):
        builder = make_source_builder(ProjectType.APP, "foo")
        self.assertIsInstance(builder, AppSourceBuilder)

    def test_source_builder_factory_returns_a_lib_builder(self):
        builder = make_source_builder(ProjectType.LIB, "foo")
        self.assertIsInstance(builder, LibSourceBuilder)


if __name__ == '__main__':
    unittest.main()
