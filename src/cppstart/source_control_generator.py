from pathlib import Path

from file_access import FileReader
from generator import Generator


def make_source_control_generator(scm_name: str, template_root_dir: Path):
    return Generator({}, FileReader(template_root_dir / scm_name))
