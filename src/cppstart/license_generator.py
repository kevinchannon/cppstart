from abc import ABC, abstractmethod


class LicenseGeneratorFactory:
    def __init__(self, licences: dict[str, str], default: str):
        self._licenses = licences
        self._default = default

    @property
    def default_license(self):
        return self._default

    def available_licenses(self):
        return [k for k in self._licenses]
