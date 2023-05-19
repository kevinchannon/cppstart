import unittest
from parameterized import parameterized
from pathlib import Path

from source_generator import *
from file_info import FileInfo


class SourceBuilderTests(unittest.TestCase):
    @parameterized.expand([
        AppSourceGenerator("foo"),
        LibSourceGenerator("foo")
    ])
    def test_adds_include_file(self, builder):
        files = builder.run()

        expected = next((f for f in files if f.path == Path("include/foo/foo.hpp")), None)
        self.assertIsNotNone(expected)
        self.assertEqual(expected.content, "#include <cstdint>\n")

    def test_lib_adds_example_files(self):
        files = LibSourceGenerator("foo").run()

        expected = next((f for f in files if f.path == Path("examples/main.cpp")), None)
        self.assertIsNotNone(expected)
        self.assertEqual(expected.content,
                         "#include <foo/foo.hpp>\n\nauto main() -> int {\n    return 0;\n}\n")

    def test_app_doesnt_add_example_files(self):
        files = AppSourceGenerator("foo").run()

        expected = next((f for f in files if f.path == Path("examples/main.cpp")), None)
        self.assertIsNone(expected)

    @parameterized.expand([
        AppSourceGenerator("foo"),
        LibSourceGenerator("foo")
    ])
    def test_adds_source_files(self, builder):
        files = builder.run()

        expected = next((f for f in files if f.path == Path("src/foo/foo.cpp")), None)
        self.assertIsNotNone(expected)
        self.assertEqual(expected.content, "#include <foo/foo.hpp>\n")

    def test_app_source_builder_adds_main(self):
        files = AppSourceGenerator("foo").run()

        expected = next((f for f in files if f.path == Path("src/main.cpp")), None)
        self.assertIsNotNone(expected)
        self.assertEqual(expected.content,
                         "#include <foo/foo.hpp>\n\nauto main() -> int {\n    return 0;\n}\n")

    def test_lib_source_builder_does_not_add_main(self):
        files = LibSourceGenerator("foo").run()

        expected = next((f for f in files if f.path == Path("src/main.cpp")), None)
        self.assertIsNone(expected)

    def test_app_source_builder_does_not_add_examples(self):
        files = AppSourceGenerator("foo").run()

        expected = next((f for f in files if f.path == Path("examples/main.cpp")), None)
        self.assertIsNone(expected)

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
        files = builder.run()

        expected = next((f for f in files if f.path == Path("src/foo/foo.cpp")), None)
        self.assertEqual(expected.content,
                         "// The license!\n// Another license line.\n\n#include <foo/foo.hpp>\n")

    def test_source_preamble_has_correct_spdx_id(self):
        self.assertTrue("SPDX-License-Identifier: spdx-ID" in get_source_code_preamble("spdx-ID", "", ""))

    def test_source_preamble_has_correct_copyright_year_and_name(self):
        self.assertTrue("Copyright (c) 2023 Mr. Foo B Baz" in get_source_code_preamble("", str(2023), "Mr. Foo B Baz"))


if __name__ == '__main__':
    unittest.main()
