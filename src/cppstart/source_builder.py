from pathlib import Path
from shutil import copytree
import os
from typing import Dict
from pathlib import Path


class SourceBuilder:
    _INCLUDE = """#include <cstdint>\n"""
    _EXAMPLES_MAIN = "#include <proj_name/proj_name.hpp>\n\nauto main() -> int {\n    return 0;\n}\n"

    def __init__(self, output_root: Path):
        self._output_root = output_root

    def get_content(self) -> Dict[Path, str]:
        proj_name = self._output_root.name
        return {self._output_root / "include" / proj_name / f"{proj_name}.hpp": self._INCLUDE,
                self._output_root / "examples" / "main.cpp": self._EXAMPLES_MAIN}
