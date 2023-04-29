import unittest

from src.cppstart.license_generator import *


class LicenseGeneratorFactoryTests(unittest.TestCase):
    def test_lists_available_licenses(self):
        self.assertEqual(["MIT", "LGPL3"],
                         LicenseGeneratorFactory({"MIT": "MIT text", "LGPL3": "LGPL3 text"}, "MIT").available_licenses())

    def test_default_id_is_correct(self):
        self.assertEqual("MIT",
                         LicenseGeneratorFactory(licences={"MIT": "MIT text", "LGPL3": "LGPL3 text"}, default="MIT").default_license)


if __name__ == '__main__':
    unittest.main()
