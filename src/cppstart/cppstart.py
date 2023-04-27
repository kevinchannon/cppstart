import argparse
from pathlib import Path

from source_builder import *
from project_type import ProjectType


class CppStart:
    def __init__(self, source_builder: SourceBuilder):
        self._source_builder = source_builder


def make_cppstart(args) -> CppStart:
    return CppStart(make_source_builder(args.project_type, Path(args.output_directory)))


def get_command_line_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("proj_name", help="name of the project")
    parser.add_argument("-d", "--output-directory", default=".", help="output directory")

    proj_types = parser.add_mutually_exclusive_group()
    proj_types.add_argument("-A", "--app", action="store_const", dest="project_type", const=ProjectType.APP,
                            help="create an application project")
    proj_types.add_argument("-L", "--lib", action="store_const", dest="project_type", const=ProjectType.LIB,
                            help="create a library project")
    proj_types.set_defaults(project_type=ProjectType.APP)

    return parser


def main():
    app = make_cppstart(get_command_line_parser().parse_args())


if __name__ == "__main__":
    main()
