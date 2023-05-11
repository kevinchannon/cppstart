import argparse
import configparser
from pathlib import Path
from datetime import datetime
import appdirs

from source_generator import *
from build_system_generator import *
from generator import *
from project_type import ProjectType
from file_access import FileReadWriter
from license_generator import *
from config import Config

PKG_DIR_PATH = Path(__file__).absolute().parent
LICENSE_TEMPLATES_DIR = PKG_DIR_PATH / "templates/licenses"
BUILD_SYSTEM_TEMPLATES_DIR = PKG_DIR_PATH / "templates/build_system"
CONFIG_DIR = Path(appdirs.user_config_dir(appname="cppstart", appauthor=False))


class CppStart:
    def __init__(self, source_generator: SourceGenerator, build_system_generator: Generator):
        self._source_generator = source_generator
        self._templated_generators = [build_system_generator]

    def run(self, file_writer: FileReadWriter):
        file_writer.write(self._source_generator.run())
        for generator in self._templated_generators:
            generator.run()


def make_cppstart(args, config: Config) -> CppStart:
    return CppStart(make_source_generator(args.project_type, args.proj_name,
                                          get_source_code_preamble(spdx_id=get_license(args).spdx_id,
                                                                   year=str(datetime.now().year),
                                                                   copyright_name=get_copyright_name(args, config))),
                    make_build_system_generator(args.build_system, args.proj_name, BUILD_SYSTEM_TEMPLATES_DIR))


def get_license(args) -> License:
    return LicenseGenerator(licences=get_license_paths(LICENSE_TEMPLATES_DIR), default="MIT",
                            file_reader=FileReader(LICENSE_TEMPLATES_DIR)).get(args.license)


def get_copyright_name(args, config: Config) -> str:
    if args.copyright_name is not None:
        return args.copyright_name

    if config.has("user", "copyright_name"):
        return config.get("user", "copyright_name")

    new_copyright_name = input("No user config. Enter your name (i.e. 'Stan Smith')\n>")
    config.set("user", "copyright_name", new_copyright_name)
    config.save()

    return new_copyright_name


def get_command_line_parser(available_licenses: list[str]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("proj_name", help="name of the project")

    proj_types = parser.add_mutually_exclusive_group()
    proj_types.add_argument("-A", "--app", action="store_const", dest="project_type", const=ProjectType.APP,
                            help="create an application project")
    proj_types.add_argument("-L", "--lib", action="store_const", dest="project_type", const=ProjectType.LIB,
                            help="create a library project")
    proj_types.set_defaults(project_type=ProjectType.APP)

    parser.add_argument("-b", "--build-system", default="cmake", help="the type of build system that the project is going to use")
    parser.add_argument("-c", "--copyright-name", help="name that will be used in copyright info")
    parser.add_argument("-d", "--output-directory", default=".", help="output directory")
    parser.add_argument("-l", "--license", choices=available_licenses, default="MIT",
                        help="the license that will be used in the project")

    return parser


def get_config(file_access: FileReadWriter) -> Config:
    config = Config(Path("config.ini"), file_access)
    if file_access.exists(Path("config.ini")):
        config.load()

    return config
