from pathlib import Path
import os

from file_access import FileReader


class LicenseGeneratorException(Exception):
    pass


class License:
    def __init__(self, spdx_id: str, text: str):
        self._spdx_id = spdx_id
        self._text = text

    @property
    def spdx_id(self):
        return self._spdx_id

    @property
    def text(self):
        return self._text


class LicenseGenerator:
    def __init__(self, licences: list[str], default: str, file_reader: FileReader):
        if default not in licences:
            raise LicenseGeneratorException(f"'{default}' is not an available license")

        self._licenses = licences
        self._default = default
        self._file_reader = file_reader

    @property
    def default_license(self):
        return self._default

    @property
    def available_licenses(self):
        return self._licenses

    def get(self, spdx_id: str) -> License:
        return License(spdx_id, self._file_reader.read(Path(spdx_id)))


def get_license_paths(root_dir: Path) -> list[str]:
    return [f for f in os.listdir(root_dir) if os.path.isfile(root_dir / f)]
