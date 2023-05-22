from pathlib import Path
import os

from file_access import FileReader, FileReadWriter
from generator import Generator
from file_info import FileInfo


class LicenseGenerator(Generator):
    def __init__(self, spdx_id: str, year: str, copyright_name: str, file_reader: FileReader):
        super().__init__({"$year": year, "$copyright_name": copyright_name}, file_reader)

        self._spdx_id = spdx_id

    @property
    def spdx_id(self):
        return self._spdx_id

    def run(self) -> set[FileInfo]:
        all_files = super().run()
        license_file = next((f for f in all_files if f.path.name == self._spdx_id), None)

        return {license_file}


def make_license_generator(spdx_id: str, license_templates_dir: Path, year: str, copyright_name: str) -> LicenseGenerator:
    return LicenseGenerator(spdx_id, year, copyright_name, FileReader(license_templates_dir))


def get_license_paths(root_dir: Path) -> list[str]:
    return [f for f in os.listdir(root_dir) if os.path.isfile(root_dir / f)]
