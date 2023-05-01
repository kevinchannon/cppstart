import unittest

from src.cppstart.build_system_generator import *


class CMakeGeneratorTests(unittest.TestCase):
    def test_top_level_cmakelists_is_created(self):
        generator = CMakeGenerator("foo")
        contents = generator.run()

        self.assertTrue(Path("CMakeLists.txt") in contents)
        self.assertTrue("foo" in contents[Path("CMakeLists.txt")])


if __name__ == '__main__':
    unittest.main()
