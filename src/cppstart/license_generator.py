from abc import ABC, abstractmethod


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
