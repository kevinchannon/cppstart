import unittest
from unittest.mock import patch, MagicMock, call
import git

from source_control_generator import *
from file_info import FileInfo


class GitGeneratorTests(unittest.TestCase):
    def test_reads_the_expected_template(self):
        template_files = {
            FileInfo(Path("template.gitignore"), "Things to ignore")
        }

        with patch.object(FileReader, "read_all", return_value=template_files) as fake_read_fn:
            generator = make_source_control_generator("git", Path("root"))
            contents = generator.run()

        self.assertEqual(Path("root/git"), generator._template_reader.root_directory)

        for expected, actual in zip({FileInfo(Path(".gitignore"), "Things to ignore")}, contents):
            self.assertEqual(expected, actual)

    def test_initialise_records_current_directory(self):
        class FakeRepo:
            class Git:
                add = MagicMock()

            class Index:
                commit = MagicMock()

            def __init__(self):
                self.git = FakeRepo.Git()
                self.index = FakeRepo.Index()

        fake_repo = FakeRepo()

        with patch.object(GitSourceControlGenerator, "scm", return_value=fake_repo),\
                patch("os.getcwd", lambda: "orig/dir"), patch("os.chdir", lambda x: None):
            gen = make_source_control_generator("git", Path("root"))
            gen.initialise(Path("repo/root"))

        self.assertEqual(1, fake_repo.git.add.call_count)
        self.assertEqual(call(all=True), fake_repo.git.add.call_args)

        self.assertEqual(1, fake_repo.index.commit.call_count)
        self.assertEqual(call("Initial commit"), fake_repo.index.commit.call_args)


if __name__ == '__main__':
    unittest.main()
