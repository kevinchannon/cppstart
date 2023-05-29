import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized

from dependency_management_generator import *
from file_info import FileInfo
from project_type import ProjectType


class ConanGeneratorTests(unittest.TestCase):
    def test_returns_expected_generator_type_for_lib_projects(self):
        with self.subTest("Conan deps with meson build system"):
            generator = make_dependency_management_generator("conan", "meson", ProjectType.LIB, Path("root"))
            self.assertIsInstance(generator, ConanDepsMgmtGenerator)

        with self.subTest("Conan deps with cmake build system"):
            generator = make_dependency_management_generator("conan", "cmake", ProjectType.LIB, Path("root"))
            self.assertIsInstance(generator, ConanCmakeBasedLibDepsMgmtGenerator)

    def test_returns_expected_generator_type_for_app_projects(self):
        with self.subTest("Conan deps with meson build system"):
            generator = make_dependency_management_generator("conan", "meson", ProjectType.APP, Path("root"))
            self.assertIsInstance(generator, ConanDepsMgmtGenerator)

        with self.subTest("Conan deps with cmake build system"):
            generator = make_dependency_management_generator("conan", "cmake", ProjectType.APP, Path("root"))
            self.assertIsInstance(generator, ConanAppDepsMgmtGenerator)

    def test_unsupported_dependency_management_system_raises_DepsManagementError(self):
        with self.subTest("for a lib project"):
            with self.assertRaises(DepsManagementError):
                _ = make_dependency_management_generator("unknown", "cmake", ProjectType.LIB, Path("root"))

        with self.subTest("for an app project"):
            with self.assertRaises(DepsManagementError):
                _ = make_dependency_management_generator("unknown", "cmake", ProjectType.APP, Path("root"))

    def test_reads_the_expected_template(self):
        template_files = {
            FileInfo(Path("conanfile.txt"), "[requires]\ncatch2/3.3.2\n\n[generators]\n$build_sys_name\n"),
            FileInfo(Path("other/file/path.txt"), "template\n\n\nsome contents")
        }

        with patch.object(FileReader, "read_all", return_value=template_files) as fake_read_fn:
            generator = make_dependency_management_generator("conan", "meson", ProjectType.APP, Path("root"))
            contents = generator.run()

        self.assertEqual(Path("root/conan"), generator._template_reader.root_directory)

        self.assertEqual(2, len(contents))
        self.assertIn(FileInfo(Path("conanfile.txt"), "[requires]\ncatch2/3.3.2\n\n[generators]\nmeson\n"), contents)
        self.assertIn(FileInfo(Path("other/file/path.txt"), "template\n\n\nsome contents"), contents)

    def test_init_files_are_executable(self):
        template_files = {
            FileInfo(Path("conanfile.txt"), "content", 0o644),
            FileInfo(Path("conanfile.cmake.rename_to_py"), "content", 0o644),
            FileInfo(Path("init.sh"), "init", 0o644),
            FileInfo(Path("init.ps1"), "init", 0o644)
        }

        for name, project_type in [("Lib project", ProjectType.LIB), ("App project", ProjectType.APP)]:
            with self.subTest(name):
                with patch.object(FileReader, "read_all", return_value=template_files):
                    generator = make_dependency_management_generator("conan", "cmake", project_type, Path("root"))
                    files = generator.run()

                for file_name, path in [("bash script", Path("init.sh")), ("powershell script", Path("init.ps1"))]:
                    with self.subTest(file_name):
                        script = next((f for f in files if f.path == path), None)
                        self.assertIsNotNone(script)
                        self.assertEqual(0o755, script.permissions)

    def test_conan_cmake_creates_correct_files_for_project_type(self):
        template_files = {
            FileInfo(Path("conanfile.txt"), "content", 0o644),
            FileInfo(Path("conanfile1.cmake.rename_to_py"), "content", 0o644),
            FileInfo(Path("conanfile2.other.rename_to_py"), "content", 0o644),
            FileInfo(Path("init.sh"), "init", 0o644),
            FileInfo(Path("init.ps1"), "init", 0o644)
        }

        with self.subTest("Lib project"):
            with patch.object(FileReader, "read_all", return_value=template_files):
                generator = make_dependency_management_generator("conan", "cmake", ProjectType.LIB, Path("root"))
                files = generator.run()

            self.assertIn(FileInfo(Path("conanfile1.py"), "content", 0o644), files)
            self.assertIn(FileInfo(Path("init.sh"), "init", 0o644), files)
            self.assertIn(FileInfo(Path("init.ps1"), "init", 0o644), files)

            self.assertNotIn(FileInfo(Path("conanfile.txt"), "content", 0o644), files)
            self.assertNotIn(FileInfo(Path("conanfile2.other.py"), "content", 0o644), files)
            self.assertNotIn(FileInfo(Path("conanfile2.other.rename_to_py"), "content", 0o644), files)

        with self.subTest("App project"):
            with patch.object(FileReader, "read_all", return_value=template_files):
                generator = make_dependency_management_generator("conan", "cmake", ProjectType.APP, Path("root"))
                files = generator.run()

            self.assertIn(FileInfo(Path("conanfile.txt"), "content", 0o644), files)
            self.assertIn(FileInfo(Path("init.sh"), "init", 0o644), files)
            self.assertIn(FileInfo(Path("init.ps1"), "init", 0o644), files)

            self.assertNotIn(FileInfo(Path("conanfile1.cmake.rename_to_py"), "content", 0o644), files)
            self.assertNotIn(FileInfo(Path("conanfile2.other.rename_to_py"), "content", 0o644), files)
            self.assertNotIn(FileInfo(Path("conanfile1.py"), "content", 0o644), files)
            self.assertNotIn(FileInfo(Path("conanfile2.py"), "content", 0o644), files)

    def test_renames_python_files_when_building_conan_generator_for_cmake_lib_projects(self):
        template_files = {
            FileInfo(Path("dir/file1.cmake.rename_to_py"), "File 1 content"),
            FileInfo(Path("conanfile.txt"), "File 2 content"),
            FileInfo(Path("dir/file3.cmake.rename_to_py"), "File 3 content")
        }

        with patch.object(FileReader, "read_all", return_value=template_files) as fake_read_fn:
            generator = make_dependency_management_generator("conan", "cmake", ProjectType.LIB, Path("root"))
            files = generator.run()

        self.assertGreaterEqual(2, len(files))

        self.assertIn(FileInfo(Path("dir/file1.py"), "File 1 content"), files)
        self.assertIn(FileInfo(Path("dir/file3.py"), "File 3 content"), files)

    def test_removes_python_files_when_building_conan_generator_for_cmake_app_projects(self):
        template_files = {
            FileInfo(Path("dir/file1.cmake.rename_to_py"), "File 1 content"),
            FileInfo(Path("conanfile.txt"), "File 2 content"),
            FileInfo(Path("dir/file3.cmake.rename_to_py"), "File 3 content")
        }

        with patch.object(FileReader, "read_all", return_value=template_files) as fake_read_fn:
            generator = make_dependency_management_generator("conan", "cmake", ProjectType.APP, Path("root"))
            files = generator.run()

        self.assertEqual(1, len(files))

        self.assertNotIn(FileInfo(Path("dir/file1.py"), "File 1 content"), files)
        self.assertNotIn(FileInfo(Path("dir/file3.py"), "File 3 content"), files)

        self.assertIn(FileInfo(Path("conanfile.txt"), "File 2 content"), files)

    def test_updates_init_files_correctly(self):
        template_files = {
            FileInfo(Path("conanfile.txt"), "content", 0o644),
            FileInfo(Path("conanfile.cmake.rename_to_py"), "content", 0o644),
            FileInfo(Path("init.sh"), "init shell\n##> APP ONLY :app only\n##> LIB ONLY :lib only", 0o644),
            FileInfo(Path("init.ps1"), "init Powershell\n##> APP ONLY :app only\n##> LIB ONLY :lib only", 0o644)
        }

        with self.subTest("Lib projects"):
            with patch.object(FileReader, "read_all", return_value=template_files):
                generator = make_dependency_management_generator("conan", "cmake", ProjectType.LIB, Path("root"))
                files = generator.run()

            for file_name, path in [("bash script", Path("init.sh")), ("powershell script", Path("init.ps1"))]:
                with self.subTest(file_name):
                    script = next((f for f in files if f.path == path), None)
                    self.assertIn("lib only", script.content)
                    self.assertNotIn("##> LIB ONLY :", script.content)
                    self.assertNotIn("##> APP ONLY :", script.content)
                    self.assertNotIn("app only", script.content)

            with self.subTest("App projects"):
                with patch.object(FileReader, "read_all", return_value=template_files):
                    generator = make_dependency_management_generator("conan", "cmake", ProjectType.APP, Path("root"))
                    files = generator.run()

                for file_name, path in [("bash script", Path("init.sh")), ("powershell script", Path("init.ps1"))]:
                    with self.subTest(file_name):
                        script = next((f for f in files if f.path == path), None)
                        self.assertIn("app only", script.content)
                        self.assertNotIn("##> APP ONLY :", script.content)
                        self.assertNotIn("##> LIB ONLY :", script.content)
                        self.assertNotIn("lib only", script.content)



if __name__ == '__main__':
    unittest.main()
