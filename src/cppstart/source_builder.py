from pathlib import Path
from shutil import copytree
import os
from typing import Dict
from pathlib import Path
from enum import Enum


class __SourceBuilder:
    _INCLUDE = """#include <cstdint>\n"""
    _EXAMPLES_MAIN = "#include <proj_name/proj_name.hpp>\n\nauto main() -> int {\n    return 0;\n}\n"

    def __init__(self, output_root: Path):
        self._output_root = output_root
        self._proj_name = self._output_root.name

    def get_content(self) -> Dict[Path, str]:
        return {self._output_root / "include" / self._proj_name / f"{self._proj_name}.hpp": self._INCLUDE,
                self._output_root / "examples" / "main.cpp": self._EXAMPLES_MAIN}


class AppSourceBuilder(__SourceBuilder):
    _PROJ_SRC = "#include <proj_name/proj_name.hpp>\n"
    _PROJ_MAIN = "#include <proj_name/proj_name.hpp>\n\nauto main() -> int {\n    return 0;\n}\n"

    def get_content(self):
        base_content = super().get_content()
        return {**base_content,
                self._output_root / "src" / self._proj_name / f"{self._proj_name}.cpp": self._PROJ_SRC,
                self._output_root / "src" / "main.cpp": self._PROJ_MAIN}


class LibSourceBuilder(__SourceBuilder):
    _PROJ_SRC = "#include <proj_name/proj_name.hpp>\n"

    def get_content(self):
        base_content = super().get_content()
        return {**base_content,
                self._output_root / "src" / self._proj_name / f"{self._proj_name}.cpp": self._PROJ_SRC}


class ProjectType(Enum):
    APP = 0
    LIB = 1


def make_source_builder(project_type: ProjectType, root_dir: Path):
    if ProjectType.APP == project_type:
        return AppSourceBuilder(root_dir)
    if ProjectType.LIB == project_type:
        return LibSourceBuilder(root_dir)
