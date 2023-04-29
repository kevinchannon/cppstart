from abc import ABC, abstractmethod


class LicenseGenerator(ABC):

    @abstractmethod
    def spdx_id(self) -> str:
        pass


class MITLicenseGenerator(LicenseGenerator):
    def spdx_id(self) -> str:
        return "MIT"
