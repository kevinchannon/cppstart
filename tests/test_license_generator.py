import unittest

from src.cppstart.license_generator import *


class LicenseGeneratorFactoryTests(unittest.TestCase):
    def test_lists_available_licenses(self):
        self.assertEqual(["MIT", "LGPL3"], LicenseGeneratorFactory(["MIT", "LGPL3"], "MIT").available_licenses)

    def test_default_id_is_correct(self):
        self.assertEqual("MIT", LicenseGeneratorFactory(licences=["MIT", "LGPL3"], default="MIT").default_license)

    def test_raises_license_generator_factory_exception_if_default_is_invalid(self):
        with self.assertRaises(LicenseGeneratorFactoryException):
            licenses = LicenseGeneratorFactory(licences=["MIT"], default="invalid")


class GetLicensePathsTests(unittest.TestCase):
    def test_gets_all_licenses_in_template_dir(self):
        license_ids = get_license_paths(Path("../src/cppstart/templates/licenses"))
        self.assertTrue("AGPL-3.0-or-later" in license_ids)
        self.assertTrue("Apache-2.0" in license_ids)
        self.assertTrue("BSL-1.0" in license_ids)
        self.assertTrue("GPL-3.0-or-later" in license_ids)
        self.assertTrue("LGPL-3.0-or-later" in license_ids)
        self.assertTrue("MIT" in license_ids)
        self.assertTrue("MPL-2.0" in license_ids)
        self.assertTrue("Unlicense" in license_ids)


if __name__ == '__main__':
    unittest.main()
