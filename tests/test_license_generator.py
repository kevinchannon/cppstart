import unittest

from src.cppstart.license_generator import *


class LicenseGeneratorFactoryTests(unittest.TestCase):
    def test_lists_available_licenses(self):
        self.assertEqual(["MIT", "LGPL3"],
                         LicenseGeneratorFactory({"MIT": "MIT text", "LGPL3": "LGPL3 text"},
                                                 "MIT").available_licenses())

    def test_default_id_is_correct(self):
        self.assertEqual("MIT",
                         LicenseGeneratorFactory(licences={"MIT": "MIT text", "LGPL3": "LGPL3 text"},
                                                 default="MIT").default_license)

    def test_raises_license_generator_factory_exception_if_default_is_invalid(self):
        with self.assertRaises(LicenseGeneratorFactoryException):
            licenses = LicenseGeneratorFactory(licences={"MIT": "text"}, default="invalid")


if __name__ == '__main__':
    unittest.main()
