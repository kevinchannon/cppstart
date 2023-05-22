import unittest
from unittest.mock import MagicMock

from license_generator import *
from cpp_start import LICENSE_TEMPLATES_DIR


class LicenseGeneratorTests(unittest.TestCase):
    _file_reader = FileReader(LICENSE_TEMPLATES_DIR)

    def setUp(self) -> None:
        self._file_reader.read = MagicMock(return_value="Some license text")

    def test_reads_license_file_from_dir(self):
        license_file = LicenseGenerator("MIT", "", "", self._file_reader).run().pop()
        self.assertEqual("MIT", license_file.path.name)

        self.assertTrue(license_file.content.startswith("MIT License"))

    def test_mit_license_has_substitutions(self):
        mit_license = make_license_generator("MIT", LICENSE_TEMPLATES_DIR, "2023", "Foo B Baz").run().pop()
        self.assertIn("Copyright (c) 2023 Foo B Baz", mit_license.content)




class GetLicensePathsTests(unittest.TestCase):
    def test_gets_all_licenses_in_template_dir(self):
        license_ids = get_license_paths(LICENSE_TEMPLATES_DIR)
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
