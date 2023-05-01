import unittest
from parameterized import parameterized

from src.cppstart.build_system_generator import *


class CMakeGeneratorTests(unittest.TestCase):
    def test_top_level_cmakelists_is_created(self):
        generator = CMakeGenerator("foo")
        contents = generator.run()

        self.assertTrue(Path("CMakeLists.txt") in contents)
        self.assertTrue("foo" in contents[Path("CMakeLists.txt")])


class MakeBuildSystemGeneratorTests(unittest.TestCase):
    @parameterized.expand([
        (BuildSystemType.CMAKE, CMakeGenerator)
    ])
    def test_returns_correct_generator_for_specified_type(self, build_sys_type, obj_type):
        gen = make_build_system_generator(build_sys_type, "foo")
        self.assertTrue(isinstance(gen, obj_type))


if __name__ == '__main__':
    unittest.main()
