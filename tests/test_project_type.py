import unittest

from project_type import *


class ProjectTypeTests(unittest.TestCase):
    def test_lib_type_from_string_works(self):
        self.assertEqual(ProjectType.LIB, project_type_from_string("lib"))
        self.assertEqual(ProjectType.LIB, project_type_from_string("LIB"))
        self.assertEqual(ProjectType.LIB, project_type_from_string(ProjectType.LIB.name))

    def test_app_type_from_string_works(self):
        self.assertEqual(ProjectType.APP, project_type_from_string("app"))
        self.assertEqual(ProjectType.APP, project_type_from_string("APP"))
        self.assertEqual(ProjectType.APP, project_type_from_string(ProjectType.APP.name))
