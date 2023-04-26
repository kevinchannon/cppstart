import argparse

from source_builder import *


def get_command_line_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("proj_name", help="name of the project")
    parser.add_argument("-d", "--output_directory", default=".", help="output directory")

    return parser


def main():
    args = get_command_line_parser().parse_args()


if __name__ == "__main__":
    main()
