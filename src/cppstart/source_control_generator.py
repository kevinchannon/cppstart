from pathlib import Path
import abc
import os
import git
from contextlib import contextmanager

from file_access import FileReader
from file_info import FileInfo
from generator import Generator


@contextmanager
def pushd(dir: Path):
    original_dir = os.getcwd()
    os.chdir(dir)

    yield

    os.chdir(original_dir)


class SourceControlGenerator(Generator):
    @abc.abstractmethod
    def initialise(self, repo_root_dir: Path):
        pass

    @abc.abstractmethod
    def email(self) -> str:
        pass


class GitSourceControlGenerator(SourceControlGenerator):
    def run(self) -> set[FileInfo]:
        files = super().run()

        gitignore_file = next((f for f in files if f.path == Path("template.gitignore")), None)
        assert(gitignore_file is not None)
        gitignore_file.path = Path(".gitignore")

        return files

    @staticmethod
    def scm():
        return git.Repo.init(os.getcwd())

    def initialise(self, repo_root_dir: Path):
        with pushd(repo_root_dir):
            repo = self.scm()
            repo.git.add(all=True)
            repo.index.commit("Initial commit")

    def email(self) -> str:
        return ""



def make_source_control_generator(scm_name: str, template_root_dir: Path):
    return GitSourceControlGenerator({}, FileReader(template_root_dir / scm_name))
