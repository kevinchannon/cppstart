import argparse
import configparser
from pathlib import Path
from datetime import datetime
import appdirs

from source_generator import *
from build_system_generator import *
from dependency_management_generator import *
from source_control_generator import *
from ci_generator import *
from generator import *
from project_type import ProjectType
from file_access import FileReadWriter
from license_generator import *
from packaging_system_generator import *
from config import Config

PKG_DIR_PATH = Path(__file__).absolute().parent
LICENSE_TEMPLATES_DIR = PKG_DIR_PATH / "templates/licenses"
BUILD_SYSTEM_TEMPLATES_DIR = PKG_DIR_PATH / "templates/build_system"
DEPENDENCY_MANAGER_TEMPLATES_DIR = PKG_DIR_PATH / "templates/deps_mgmt"
SOURCE_CONTROL_TEMPLATES_DIR = PKG_DIR_PATH / "templates/source_control"
CI_TEMPLATES_DIR = PKG_DIR_PATH / "templates/ci"
PACKAGING_TEMPLATES_DIR = PKG_DIR_PATH / "templates/packaging"

CONFIG_DIR = Path(appdirs.user_config_dir(appname="cppstart", appauthor=False))


class CppStart:
    def __init__(self, source_generator: SourceGenerator, build_system_generator: Generator,
                 deps_mgmt_generator: Generator, scm_generator: SourceControlGenerator, ci_generator: Generator,
                 license_generator: Generator, packaging_system_generator: Generator):
        self._source_generator = source_generator
        self._templated_generators = [
            build_system_generator,
            deps_mgmt_generator,
            scm_generator,
            ci_generator,
            license_generator,
 #           packaging_system_generator,
        ]

        self._source_control_initialiser = scm_generator.initialise

    def run(self, file_writer: FileReadWriter):
        file_writer.write(self._source_generator.run())
        for generator in self._templated_generators:
            file_writer.write(generator.run())

    def initialise(self, root_directory):
        self._source_control_initialiser(root_directory)


def make_cppstart(args, config: Config) -> CppStart:
    year = str(datetime.now().year)
    license_gen = make_license_generator(args.license, LICENSE_TEMPLATES_DIR, year, get_copyright_name(args, config))
    src_control_gen = make_source_control_generator(args.source_control, SOURCE_CONTROL_TEMPLATES_DIR)
    possible_github_username = src_control_gen.email().split('@')[0]
    return CppStart(make_source_generator(args.project_type, args.proj_name,
                                          get_source_code_preamble(spdx_id=license_gen.spdx_id,
                                                                   year=year,
                                                                   copyright_name=get_copyright_name(args, config))),
                    make_build_system_generator(args.build_system, args.proj_name, args.project_type,
                                                BUILD_SYSTEM_TEMPLATES_DIR),
                    make_dependency_namagement_generator(args.dependency_management, args.build_system,
                                                         DEPENDENCY_MANAGER_TEMPLATES_DIR),
                    src_control_gen,
                    make_ci_generator(args.ci, args.proj_name, CI_TEMPLATES_DIR),
                    license_gen,
                    make_packaging_system_generator("conan", args.proj_name, args.license,
                                                    get_copyright_name(args, config), src_control_gen.email(),
                                                    f"https://github.com:{possible_github_username}/{args.proj_name}",
                                                    PACKAGING_TEMPLATES_DIR))


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

    parser.add_argument("-b", "--build-system", default="cmake",
                        help="the type of build system that the project is going to use")
    parser.add_argument("-c", "--copyright-name", help="name that will be used in copyright info")
    parser.add_argument("-d", "--dependency-management", default="conan",
                        help="the type of dependency manager that the project will use")
    parser.add_argument("-i", "--ci", default="github",
                        help="the type of CI system that the project will use")
    parser.add_argument("-l", "--license", choices=available_licenses, default="MIT",
                        help="the license that will be used in the project")
    parser.add_argument("-o", "--output-directory", default=".", help="output directory")
    parser.add_argument("-s", "--source-control", default="git",
                        help="the type of source control that the project will use")

    return parser


def get_config(file_access: FileReadWriter) -> Config:
    config = Config(Path("config.ini"), file_access)
    if file_access.exists(Path("config.ini")):
        config.load()

    return config
