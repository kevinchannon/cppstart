import unittest
from unittest.mock import MagicMock

from src.cppstart.generator import *
from src.cppstart.file_access import *


class GeneratorTests(unittest.TestCase):
    def test_replaces_single_value(self):
        template_reader = FileReader(Path("templates/root"))
        template_reader.read_all = MagicMock(
            return_value={Path("some/subdir/file.txt"): "this should be replaced: to_replace, was it?"})

        generator = Generator({"to_replace": "new_value"}, template_reader)
        files = generator.run()

        self.assertTrue(template_reader.read_all.called)
        self.assertTrue(Path("some/subdir/file.txt") in files)
        self.assertEqual(files[Path("some/subdir/file.txt")], "this should be replaced: new_value, was it?")

    def test_replaces_multiple_instances_of_the_same_value(self):
        template_reader = FileReader(Path("templates/root"))
        template_reader.read_all = MagicMock(
            return_value={Path("some/subdir/file.txt"): "replace multiple to_replaces: to_replace, was it? (to_replace)"})

        generator = Generator({"to_replace": "new_value"}, template_reader)
        files = generator.run()

        self.assertTrue(template_reader.read_all.called)
        self.assertTrue(Path("some/subdir/file.txt") in files)
        self.assertEqual(files[Path("some/subdir/file.txt")],
                         "replace multiple new_values: new_value, was it? (new_value)")

    def test_replaces_multiple_values_in_multiple_files(self):
        template_reader = FileReader(Path("templates/root"))
        template_reader.read_all = MagicMock(
            return_value={Path("a/b/c.txt"): "text with\nvalue1 and value2 to replace",
                          Path("a/d.txt"): "text with\nvalue1",
                          Path("a/e/f.txt"): "text with\nvalue3 and value2"})

        generator = Generator({"value1": "replaced1", "value2": "replaced2", "value3": "replaced3"}, template_reader)
        files = generator.run()

        self.assertEqual(1, template_reader.read_all.call_count)
        self.assertEqual({Path("a/b/c.txt"): "text with\nreplaced1 and replaced2 to replace",
                          Path("a/d.txt"): "text with\nreplaced1",
                          Path("a/e/f.txt"): "text with\nreplaced3 and replaced2"}, files)



if __name__ == '__main__':
    unittest.main()