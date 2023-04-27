from pathlib import Path
from shutil import copytree
import os
from abc import ABC, abstractmethod
from typing import Dict
from pathlib import Path

from project_type import ProjectType


class SourceBuilder(ABC):
    @abstractmethod
    def get_content(self) -> Dict[Path, str]:
        pass


class __SourceBuilder(SourceBuilder):
    _INCLUDE = """#include <cstdint>\n"""
    _EXAMPLES_MAIN = "#include <proj_name/proj_name.hpp>\n\nauto main() -> int {\n    return 0;\n}\n"

    def __init__(self, project_name: str):
        self._proj_name = project_name

    def _get_content(self) -> Dict[Path, str]:
        return {Path("include") / self._proj_name / f"{self._proj_name}.hpp": self._INCLUDE,
                Path("examples") / "main.cpp": self._EXAMPLES_MAIN}


class AppSourceBuilder(__SourceBuilder):
    _PROJ_SRC = "#include <proj_name/proj_name.hpp>\n"
    _PROJ_MAIN = "#include <proj_name/proj_name.hpp>\n\nauto main() -> int {\n    return 0;\n}\n"

    def get_content(self):
        base_content = super()._get_content()
        return {**base_content,
                Path("src") / self._proj_name / f"{self._proj_name}.cpp": self._PROJ_SRC,
                Path("src") / "main.cpp": self._PROJ_MAIN}


class LibSourceBuilder(__SourceBuilder):
    _PROJ_SRC = "#include <proj_name/proj_name.hpp>\n"

    def get_content(self):
        base_content = super()._get_content()
        return {**base_content,
                Path("src") / self._proj_name / f"{self._proj_name}.cpp": self._PROJ_SRC}


def make_source_builder(project_type: ProjectType, project_name: str):
    if ProjectType.APP == project_type:
        return AppSourceBuilder(project_name)
    if ProjectType.LIB == project_type:
        return LibSourceBuilder(project_name)
