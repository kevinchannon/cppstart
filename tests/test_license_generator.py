import unittest

from src.cppstart.license_generator import *


class LicenseGeneratorFactoryTests(unittest.TestCase):
    def test_lists_available_licenses(self):
        self.assertEqual(["MIT", "LGPL3"], LicenseGeneratorFactory({"MIT": "MIT text", "LGPL3": "LGPL3 text"}).available_licenses())


if __name__ == '__main__':
    unittest.main()
