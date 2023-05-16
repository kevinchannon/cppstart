from pathlib import Path

from file_access import FileReader
from file_info import FileInfo
from generator import Generator


class GitSourceControlGenerator(Generator):
    def run(self) -> set[FileInfo]:
        files = super().run()

        gitignore_file = next((f for f in files if f.path == Path("template.gitignore")), None)
        assert(gitignore_file is not None)
        gitignore_file.path = Path(".gitignore")

        return files


def make_source_control_generator(scm_name: str, template_root_dir: Path):
    return GitSourceControlGenerator({}, FileReader(template_root_dir / scm_name))
