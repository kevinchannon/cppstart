import unittest
from unittest.mock import patch, MagicMock

from src.cppstart.source_control_generator import *


class GitGeneratorTests(unittest.TestCase):
    def test_reads_the_expected_template(self):
        template_files = {
            Path(".gitignore"): "Things to ignore"
        }

        with patch.object(FileReader, "read_all", return_value=template_files) as fake_read_fn:
            generator = make_source_control_generator("git", Path("root"))
            contents = generator.run()

        self.assertEqual(Path("root/git"), generator._template_reader.root_directory)

        expected_content = {
            Path(".gitignore"): "Things to ignore"
        }

        self.assertEqual(expected_content, contents)


if __name__ == '__main__':
    unittest.main()
