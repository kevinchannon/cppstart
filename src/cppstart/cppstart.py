import argparse
import configparser
from pathlib import Path
from datetime import datetime
import appdirs

from source_generator import *
from project_type import ProjectType
from file_access import FileReadWriter
from license_generator import *
from config import Config

PKG_DIR_PATH = Path(__file__).absolute().parent


class CppStart:
    def __init__(self, source_generator: SourceGenerator):
        self._source_generator = source_generator

    def run(self, file_writer: FileReadWriter):
        file_writer.write(self._source_generator.run())


def make_cppstart(args, config: Config) -> CppStart:
    return CppStart(make_source_generator(args.project_type, args.proj_name,
                                          get_source_code_preamble(spdx_id=get_license(args).spdx_id,
                                                                   year=str(datetime.now().year),
                                                                   copyright_name=get_copyright_name(args, config))))


def get_license(args) -> License:
    license_templates_dir = PKG_DIR_PATH / "templates/licenses"
    return LicenseGenerator(licences=get_license_paths(license_templates_dir), default="MIT",
                            file_reader=FileReader(license_templates_dir)).get(args.license)


def get_copyright_name(args, config: Config) -> str:
    if args.copyright_name is not None:
        return args.copyright_name

    return config.get("user", "copyright_name")


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
    parser.add_argument("-c", "--copyright-name", help="name that will be used in copyright info")

    return parser


def get_config(file_access: FileReadWriter) -> Config:
    config = Config(Path("config.ini"), file_access)
    config.load()
    return config


def main():
    args = get_command_line_parser().parse_args()
    app = make_cppstart(args,
                        get_config(FileReadWriter(Path(appdirs.user_config_dir(appname="cppstart", appauthor=False)))))
    app.run(args.output_directory)


if __name__ == "__main__":
    main()
