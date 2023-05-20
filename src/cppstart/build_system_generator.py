from pathlib import Path

from file_access import FileReader
from file_info import FileInfo
from generator import Generator
from project_type import ProjectType


class BuildSystemGenerator(Generator):
    def __init__(self, replacements:  dict[str, str], proj_type: ProjectType, template_reader: FileReader):
        super().__init__(replacements, template_reader)

        self._project_type = proj_type

    def run(self) -> set[FileInfo]:
        files = super().run()

        for p in [Path("build.sh"), Path("build.ps1")]:
            build_script = next((f for f in files if f.path == p), None)
            if build_script is not None:
                build_script.permissions = 0o755

        return files


class CMakeGenerator(BuildSystemGenerator):
    def run(self) -> set[FileInfo]:
        files = super().run()

        if self._project_type == ProjectType.LIB:
            src_cmake_file = next((f for f in files if f.path == Path("src/CMakeLists.txt")), None)
            content_to_remove = "add_executable(proj_name\n  main.cpp\n)\n"
            for old, new in self._replacements.items():
                content_to_remove = content_to_remove.replace(old, new)

            files.remove(src_cmake_file)

            src_cmake_file.content = src_cmake_file.content.replace(content_to_remove, "")
            files.add(src_cmake_file)
        elif self._project_type == ProjectType.APP:
            example_cmake_file = next((f for f in files if f.path == Path("examples/CMakeLists.txt")), None)
            files.remove(example_cmake_file)

            cmake_file = next((f for f in files if f.path == Path("CMakeLists.txt")), None)
            files.remove(cmake_file)
            cmake_file.content = cmake_file.content.replace("  add_subdirectory(examples)\n", "")
            files.add(cmake_file)

        return files


def make_build_system_generator(build_sys_name: str, proj_name: str, proj_type: ProjectType, template_root_dir: Path):
    if build_sys_name == "cmake":
        return CMakeGenerator({"proj_name": proj_name}, proj_type, FileReader(template_root_dir / build_sys_name))

    return BuildSystemGenerator({"proj_name": proj_name}, proj_type, FileReader(template_root_dir / build_sys_name))
