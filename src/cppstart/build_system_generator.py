from pathlib import Path

from file_access import FileReader
from generator import Generator


def make_build_system_generator(build_sys_name: str, proj_name: str, template_root_dir: Path):
    return Generator({"proj_name": proj_name}, FileReader(template_root_dir / build_sys_name))
