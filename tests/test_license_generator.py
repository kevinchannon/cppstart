import unittest
from unittest.mock import MagicMock

from license_generator import *
from cpp_start import LICENSE_TEMPLATES_DIR


class LicenseGeneratorTests(unittest.TestCase):
    _file_reader = FileReader()

    def setUp(self) -> None:
        self._file_reader.read = MagicMock(return_value="Some license text")

    def test_lists_available_licenses(self):
        self.assertEqual(["MIT", "LGPL3"],
                         LicenseGenerator(["MIT", "LGPL3"], "MIT",
                                          file_reader=self._file_reader).available_licenses)

    def test_default_id_is_correct(self):
        self.assertEqual("MIT", LicenseGenerator(licences=["MIT", "LGPL3"], default="MIT",
                                                 file_reader=self._file_reader).default_license)

    def test_raises_license_generator_exception_if_default_is_invalid(self):
        with self.assertRaises(LicenseGeneratorException):
            _ = LicenseGenerator(licences=["MIT"], default="invalid", file_reader=self._file_reader)

    def test_reads_license_file_from_dir(self):
        self.assertEqual("MIT",
                         LicenseGenerator(["MIT", "LGPL3"], "MIT",
                                          file_reader=self._file_reader).get("MIT").spdx_id)
        self._file_reader.read.assert_called_with(Path("MIT"))

        self.assertEqual("Some license text",
                         LicenseGenerator(["MIT", "LGPL3"], "MIT",
                                          file_reader=self._file_reader).get("MIT").text)
        self._file_reader.read.assert_called_with(Path("MIT"))


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
