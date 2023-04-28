import unittest
from parameterized import parameterized
from pathlib import Path

from src.cppstart.source_generator import *


class SourceBuilderTests(unittest.TestCase):
    @parameterized.expand([
        AppSourceGenerator("foo"),
        LibSourceGenerator("foo")
    ])
    def test_adds_include_file(self, builder):
        contents = builder.run()
        self.assertTrue(Path("include/foo/foo.hpp") in contents)
        self.assertEqual(contents[Path("include/foo/foo.hpp")], "#include <cstdint>\n")

    @parameterized.expand([
        AppSourceGenerator("foo"),
        LibSourceGenerator("foo")
    ])
    def test_adds_example_files(self, builder):
        contents = builder.run()
        self.assertTrue(Path("examples/main.cpp") in contents)
        self.assertEqual(contents[Path("examples/main.cpp")],
                         "#include <proj_name/proj_name.hpp>\n\nauto main() -> int {\n    return 0;\n}\n")

    @parameterized.expand([
        AppSourceGenerator("foo"),
        LibSourceGenerator("foo")
    ])
    def test_adds_source_files(self, builder):
        contents = builder.run()
        self.assertTrue(Path("src/foo/foo.cpp") in contents)
        self.assertEqual(contents[Path("src/foo/foo.cpp")], "#include <proj_name/proj_name.hpp>\n")

    def test_app_source_builder_adds_main(self):
        contents = AppSourceGenerator("foo").run()
        self.assertTrue(Path("src/main.cpp") in contents)
        self.assertEqual(contents[Path("src/main.cpp")],
                         "#include <proj_name/proj_name.hpp>\n\nauto main() -> int {\n    return 0;\n}\n")

    def test_lib_source_builder_does_not_add_main(self):
        contents = LibSourceGenerator("foo").run()
        self.assertFalse(Path("src/main.cpp") in contents)

    def test_source_builder_factory_returns_an_app_builder(self):
        builder = make_source_generator(ProjectType.APP, "foo")
        self.assertIsInstance(builder, AppSourceGenerator)

    def test_source_builder_factory_returns_a_lib_builder(self):
        builder = make_source_generator(ProjectType.LIB, "foo")
        self.assertIsInstance(builder, LibSourceGenerator)

    @parameterized.expand([
        ("App source builder", AppSourceGenerator("foo", "// The license!\n// Another license line.")),
        ("Lib source builder", LibSourceGenerator("foo", "// The license!\n// Another license line."))
    ])
    def test_sources_have_license_at_the_top(self, _, builder):
        contents = builder.run()
        self.assertEqual(contents[Path("src/foo/foo.cpp")],
                         "// The license!\n// Another license line.\n\n#include <proj_name/proj_name.hpp>\n")


if __name__ == '__main__':
    unittest.main()
