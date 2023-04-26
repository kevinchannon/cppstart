import argparse

from source_builder import *


def get_command_line_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("proj_name", help="name of the project")
    parser.add_argument("-d", "--output-directory", default=".", help="output directory")

    proj_types = parser.add_mutually_exclusive_group()
    proj_types.add_argument("-A", "--app", action="store_true", dest="is_app",
                            help="create an application project")
    proj_types.add_argument("-L", "--lib", action="store_true", dest="is_lib",
                            help="create a library project")

    return parser


def main():
    args = get_command_line_parser().parse_args()


if __name__ == "__main__":
    main()
