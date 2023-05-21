from pathlib import Path

from file_access import FileReader
from file_info import FileInfo
from generator import Generator
from project_type import ProjectType


def make_packaging_system_generator(pkg_sys_name: str, project_name: str, license: str, copyright_name: str,
                                    author_email: str, project_url: str, template_root_dir: Path):
    replacements = {
        "proj_name": project_name,
        "$license_name": license,
        "$copyright_name": copyright_name,
        "$author_email": author_email,
        "$url": project_url
    }
    return Generator(replacements, FileReader(template_root_dir / pkg_sys_name))
