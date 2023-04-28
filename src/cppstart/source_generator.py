from pathlib import Path
from shutil import copytree
import os
from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path

from project_type import ProjectType


class SourceGenerator(ABC):
    @abstractmethod
    def run(self) -> dict[Path, str]:
        pass


class __SourceGenerator(SourceGenerator):
    _LICENSED_SOURCE = "{}\n\n{}"
    _INCLUDE = """#include <cstdint>\n"""
    _EXAMPLES_MAIN = "#include <proj_name/proj_name.hpp>\n\nauto main() -> int {\n    return 0;\n}\n"

    def __init__(self, project_name: str, license_text):
        assert isinstance(license_text, str) or license_text is None

        self._proj_name = project_name
        self._license_text = license_text

        if self._license_text is not None:
            self._include = self._LICENSED_SOURCE.format(self._license_text, self._INCLUDE)
            self._examples_main = self._LICENSED_SOURCE.format(self._license_text, self._EXAMPLES_MAIN)
        else:
            self._include = self._INCLUDE
            self._examples_main = self._EXAMPLES_MAIN

    def run(self) -> dict[Path, str]:
        return {Path("include") / self._proj_name / f"{self._proj_name}.hpp": self._include,
                Path("examples") / "main.cpp": self._examples_main}


class AppSourceGenerator(__SourceGenerator):
    _PROJ_SRC = "#include <proj_name/proj_name.hpp>\n"
    _PROJ_MAIN = "#include <proj_name/proj_name.hpp>\n\nauto main() -> int {\n    return 0;\n}\n"

    def __init__(self, project_name: str, license_text=None):
        super().__init__(project_name, license_text)

        if self._license_text is not None:
            self._proj_src = self._LICENSED_SOURCE.format(self._license_text, self._PROJ_SRC)
            self._proj_main = self._LICENSED_SOURCE.format(self._license_text, self._PROJ_MAIN)
        else:
            self._proj_src = self._PROJ_SRC
            self._proj_main = self._PROJ_MAIN

    def run(self):
        base_content = super().run()
        return {**base_content,
                Path("src") / self._proj_name / f"{self._proj_name}.cpp": self._proj_src,
                Path("src") / "main.cpp": self._proj_main}


class LibSourceGenerator(__SourceGenerator):
    _PROJ_SRC = "#include <proj_name/proj_name.hpp>\n"

    def __init__(self, project_name: str, license_text=None):
        super().__init__(project_name, license_text)

        if self._license_text is not None:
            self._proj_src = self._LICENSED_SOURCE.format(self._license_text, self._PROJ_SRC)
        else:
            self._proj_src = self._PROJ_SRC

    def run(self):
        base_content = super().run()
        return {**base_content,
                Path("src") / self._proj_name / f"{self._proj_name}.cpp": self._proj_src}


def make_source_generator(project_type: ProjectType, project_name: str, license_text=None):
    if ProjectType.APP == project_type:
        return AppSourceGenerator(project_name, license_text)
    if ProjectType.LIB == project_type:
        return LibSourceGenerator(project_name, license_text)
