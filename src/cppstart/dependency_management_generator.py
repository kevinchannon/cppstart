from pathlib import Path

from file_access import FileReader
from file_info import FileInfo
from generator import Generator
from project_type import ProjectType


class DepsManagementError(Exception):
    pass


class DepsManagementGenerator(Generator):
    def run(self) -> set[FileInfo]:
        files = super().run()

        for p in [Path("init.sh"), Path("init.ps1")]:
            build_script = next((f for f in files if f.path == p), None)
            if build_script is not None:
                build_script.permissions = 0o755

        return files


class ConanDepsMgmtGenerator(DepsManagementGenerator):

    def _run(self, project_type: ProjectType) -> set[FileInfo]:
        files = super().run()

        assert (project_type == ProjectType.LIB or project_type == ProjectType.APP)
        replace_text = "##> LIB ONLY :" if project_type == ProjectType.LIB else "##> APP ONLY :"
        remove_line_key = "##> APP ONLY :" if project_type == ProjectType.LIB else "##> LIB ONLY :"

        for p in [Path("init.sh"), Path("init.ps1")]:
            build_script = next((f for f in files if f.path == p), None)
            if build_script is None:
                continue

            files.remove(build_script)
            build_script.content = "\n".join([line.replace(replace_text, "") for line in build_script.content.split("\n") if
                                    not line.startswith(remove_line_key)])
            files.add(build_script)

        return files


class ConanCmakeBasedLibDepsMgmtGenerator(ConanDepsMgmtGenerator):
    def __init__(self, template_reader: FileReader):
        super().__init__({}, template_reader)

    def run(self) -> set[FileInfo]:
        files = super()._run(ProjectType.LIB)

        for file in filter(lambda f: str(f.path).endswith(".cmake.rename_to_py"), files):
            files.remove(file)
            file.path = Path(str(file.path).replace(".cmake.rename_to_py", ".py"))
            files.add(file)

        # Any remaining python files must be for other build systems, so remove them now
        for file in list(filter(lambda f: str(f.path).endswith(".rename_to_py"), files)):
            files.remove(file)

        # This is the app version of the file, so we need to remove it
        text_file = next((f for f in files if f.path == Path("conanfile.txt")), None)
        files.remove(text_file)

        return files


class ConanAppDepsMgmtGenerator(ConanDepsMgmtGenerator):
    def run(self) -> set[FileInfo]:
        files = super()._run(ProjectType.APP)

        # Remove these, because they're for lib projects
        for file in list(filter(lambda f: str(f.path).endswith(".rename_to_py"), files)):
            files.remove(file)

        return files


def __make_conan_lib_deps_generator(build_sys_name: str, template_root_dir: Path):
    if build_sys_name == "cmake":
        return ConanCmakeBasedLibDepsMgmtGenerator(FileReader(template_root_dir / "conan"))
    else:
        return ConanDepsMgmtGenerator({"$build_sys_name": build_sys_name}, FileReader(template_root_dir / "conan"))


def __make_conan_generator(build_sys_name: str, project_type: ProjectType, template_root_dir: Path):
    return __make_conan_lib_deps_generator(build_sys_name, template_root_dir)
    # if project_type == ProjectType.LIB:
    #    return __make_conan_lib_deps_generator(build_sys_name, template_root_dir)
    # else:
    #    return ConanAppDepsMgmtGenerator({"$build_sys_name": build_sys_name}, FileReader(template_root_dir / "conan"))


def make_dependency_management_generator(dep_mgr_name: str, build_sys_name: str, project_type: ProjectType,
                                         template_root_dir: Path):
    if dep_mgr_name == "conan":
        gen = __make_conan_generator(build_sys_name, project_type, template_root_dir)
        return gen
    else:
        raise DepsManagementError(f"Unsupported dependency management system: {dep_mgr_name}")
