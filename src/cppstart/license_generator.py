from pathlib import Path
import os


class LicenseGeneratorFactoryException(Exception):
    pass


class LicenseGeneratorFactory:
    def __init__(self, licences: dict[str, str], default: str):
        if default not in licences:
            raise LicenseGeneratorFactoryException(f"'{default}' is not an available license")

        self._licenses = licences
        self._default = default

    @property
    def default_license(self):
        return self._default

    def available_licenses(self):
        return [k for k in self._licenses]


def get_license_paths(root_dir: Path) -> list[str]:
    return [f for f in os.listdir(root_dir) if os.path.isfile(root_dir / f)]
