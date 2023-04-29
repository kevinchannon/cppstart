import argparse
from pathlib import Path

from source_generator import *
from project_type import ProjectType
from file_writer import FileWriter


class CppStart:
    def __init__(self, source_generator: SourceGenerator, file_writer: FileWriter):
        self._source_generator = source_generator
        self._file_writer = file_writer

    def run(self):
        self._file_writer.write(self._source_generator.run())


def make_cppstart(args) -> CppStart:
    return CppStart(make_source_generator(args.project_type, args.proj_name),
                    FileWriter(args.output_directory))


def get_command_line_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("proj_name", help="name of the project")

    proj_types = parser.add_mutually_exclusive_group()
    proj_types.add_argument("-A", "--app", action="store_const", dest="project_type", const=ProjectType.APP,
                            help="create an application project")
    proj_types.add_argument("-L", "--lib", action="store_const", dest="project_type", const=ProjectType.LIB,
                            help="create a library project")
    proj_types.set_defaults(project_type=ProjectType.APP)

    parser.add_argument("-d", "--output-directory", default=".", help="output directory")
    parser.add_argument("-l", "--license", default="MIT", help="the license that will be used in the project")

    return parser


def main():
    app = make_cppstart(get_command_line_parser().parse_args())
    app.run()


if __name__ == "__main__":
    main()
