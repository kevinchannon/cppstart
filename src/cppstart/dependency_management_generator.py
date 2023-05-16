from pathlib import Path

from file_access import FileReader
from file_info import FileInfo
from generator import Generator


class DepsManagementGenerator(Generator):
    def run(self) -> set[FileInfo]:
        files = super().run()

        init_script = next((f for f in files if f.path == Path("init.sh")), None)
        assert(init_script is not None)
        init_script.permissions = 0o755

        init_script = next((f for f in files if f.path == Path("init.ps1")), None)
        assert(init_script is not None)
        init_script.permissions = 0o755

        return files

def make_dependency_namagement_generator(dep_mgr_name: str, build_sys_name: str, template_root_dir: Path):
    return DepsManagementGenerator({"build_sys_name": build_sys_name}, FileReader(template_root_dir / dep_mgr_name))
