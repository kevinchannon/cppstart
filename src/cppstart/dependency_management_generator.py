from pathlib import Path

from file_access import FileReader
from generator import Generator


def make_dependency_namagement_generator(dep_mgr_name: str, build_sys_name: str, template_root_dir: Path):
    return Generator({"build_sys_name": build_sys_name}, FileReader(template_root_dir / dep_mgr_name))
