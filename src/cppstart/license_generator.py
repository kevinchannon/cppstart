from abc import ABC, abstractmethod


class LicenseGeneratorFactory:
    def __init__(self, licences: dict[str, str]):
        self._licenses = licences

    def available_licenses(self):
        return [k for k in self._licenses]
