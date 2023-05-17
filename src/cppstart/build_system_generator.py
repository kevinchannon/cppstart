from pathlib import Path

from file_access import FileReader
from file_info import FileInfo
from generator import Generator


class BuildSystemGenerator(Generator):
    def run(self) -> set[FileInfo]:
        files = super().run()

        for p in [Path("build.sh"), Path("build.ps1")]:
            build_script = next((f for f in files if f.path == p), None)
            if build_script is not None:
                build_script.permissions = 0o755

        return files


def make_build_system_generator(build_sys_name: str, proj_name: str, template_root_dir: Path):
    return BuildSystemGenerator({"proj_name": proj_name}, FileReader(template_root_dir / build_sys_name))
