import shutil
import os
import git
from pathlib import Path
from datetime import datetime
import sys

# This feels like a hack, but the imports below don't work once the package is installed via Pip without it.
sys.path.append(str(Path(__file__).absolute().parent))
import cpp_start
import license_generator
import file_access


def rename_all_the_things(root_dir: str, proj_name: str):
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            file_path = os.path.join(root, name)
            with open(file_path, "r") as file:
                contents = file.read()

            contents = contents.replace("proj_name", proj_name)
            with open(file_path, "w") as file:
                file.write(contents)

            if "proj_name" in name:
                new_name = name.replace("proj_name", proj_name)
                new_file_path = os.path.join(root, new_name)
                os.rename(file_path, new_file_path)

        for name in dirs:
            dir_path = os.path.join(root, name)
            if "proj_name" in name:
                new_name = name.replace("proj_name", proj_name)
                new_dir_path = os.path.join(root, new_name)
                os.rename(dir_path, new_dir_path)


def copy_license_file(new_license: str, root_dir: Path, pkg_dir: Path):
    license_path = pkg_dir / "templates" / "licenses" / new_license
    shutil.copy(license_path, root_dir)
    os.remove(root_dir / "LICENSE")
    os.rename(root_dir / new_license, root_dir / "LICENSE")


def main():
    args = cpp_start.get_command_line_parser(
        license_generator.get_license_paths(cpp_start.LICENSE_TEMPLATES_DIR)).parse_args()
    config = cpp_start.get_config(file_access.FileReadWriter(cpp_start.CONFIG_DIR))

    dest_dir = Path(args.output_directory) / args.proj_name
    copy_license_file(args.license, dest_dir, cpp_start.PKG_DIR_PATH)

    app = cpp_start.make_cppstart(args, config)
    app.run(file_access.FileReadWriter(dest_dir))
    app.initialise(dest_dir)


if __name__ == "__main__":
    main()
