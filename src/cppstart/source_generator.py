from pathlib import Path
from shutil import copytree
import os
from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path

from project_type import ProjectType
from file_info import FileInfo


class SourceGenerator(ABC):
    @abstractmethod
    def run(self) -> set[FileInfo]:
        pass


class __SourceGeneratorBase(SourceGenerator):
    _LICENSED_SOURCE = "{}\n\n{}"
    _INCLUDE = "#include <cstdint>\n"
    _EXAMPLES_MAIN = \
        "#include <{0}/{0}.hpp>\n" \
        "\n" \
        "auto main() -> int {{\n" \
        "    return 0;\n" \
        "}}\n"
    _TEST_SRC = \
        "#include <{0}/{0}.hpp>\n" \
        "\n" \
        "#include <catch2/catch_test_macros.hpp>\n" \
        "\n" \
        "TEST_CASE(\"{0} tests\") {{\n" \
        "    SECTION(\"delete this require and add your own tests!\")\n" \
        "        REQUIRE(false);\n" \
        "}}\n"

    def __init__(self, project_name: str, license_text):
        assert isinstance(license_text, str) or license_text is None

        self._proj_name = project_name
        self._license_text = license_text

        if self._license_text is not None:
            self._include = self._LICENSED_SOURCE.format(self._license_text, self._INCLUDE)
            self._examples_main = self._LICENSED_SOURCE.format(self._license_text,
                                                               self._EXAMPLES_MAIN.format(self._proj_name))
            self._test_src = self._LICENSED_SOURCE.format(self._license_text, self._TEST_SRC.format(self._proj_name))
        else:
            self._include = self._INCLUDE
            self._examples_main = self._EXAMPLES_MAIN.format(self._proj_name)
            self._test_src = self._TEST_SRC.format(self._proj_name)

    def run(self) -> set[FileInfo]:
        return {FileInfo(Path("include") / self._proj_name / f"{self._proj_name}.hpp", self._include),
                FileInfo(Path("test") / f"{self._proj_name}.tests.cpp", self._test_src)}


class AppSourceGenerator(__SourceGeneratorBase):
    def __init__(self, project_name: str, license_text=None):
        super().__init__(project_name, license_text)

        proj_src = "#include <{0}/{0}.hpp>\n".format(self._proj_name)
        proj_main = "#include <{0}/{0}.hpp>\n\nauto main() -> int {{\n    return 0;\n}}\n".format(self._proj_name)

        if self._license_text is not None:
            self._proj_src = self._LICENSED_SOURCE.format(self._license_text, proj_src)
            self._proj_main = self._LICENSED_SOURCE.format(self._license_text, proj_main)
        else:
            self._proj_src = proj_src
            self._proj_main = proj_main

    def run(self) -> set[FileInfo]:
        base_content = super().run()
        return {*base_content,
                FileInfo(Path("src") / self._proj_name / f"{self._proj_name}.cpp", self._proj_src),
                FileInfo(Path("src") / "main.cpp", self._proj_main)}


class LibSourceGenerator(__SourceGeneratorBase):
    def __init__(self, project_name: str, license_text=None):
        super().__init__(project_name, license_text)

        proj_src = "#include <{}/{}.hpp>\n".format(self._proj_name, self._proj_name)

        if self._license_text is not None:
            self._proj_src = self._LICENSED_SOURCE.format(self._license_text, proj_src)
        else:
            self._proj_src = proj_src

    def run(self) -> set[FileInfo]:
        base_content = super().run()
        return {*base_content,
                FileInfo(Path("examples") / "main.cpp", self._examples_main),
                FileInfo(Path("src") / self._proj_name / f"{self._proj_name}.cpp", self._proj_src)}


def make_source_generator(project_type: ProjectType, project_name: str, license_text=None):
    if ProjectType.APP == project_type:
        return AppSourceGenerator(project_name, license_text)
    if ProjectType.LIB == project_type:
        return LibSourceGenerator(project_name, license_text)


def get_source_code_preamble(spdx_id: str, year: str, copyright_name: str):
    return f"/*\n* SPDX-License-Identifier: {spdx_id}\n*\n* Copyright (c) {year} {copyright_name}\n*\n*/"
