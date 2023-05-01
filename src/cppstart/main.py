import shutil
import os
import git
from pathlib import Path
from datetime import datetime
import sys


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


def license_choices(pkg_dir_path: str):
    license_dir_path = os.path.join(pkg_dir_path, "templates", "licenses")
    return [f for f in os.listdir(license_dir_path) if os.path.isfile(os.path.join(license_dir_path, f))]


def copy_license_file(new_license: str, root_dir: Path, pkg_dir: Path):
    license_path = pkg_dir / "templates" / "licenses" / new_license
    shutil.copy(license_path, root_dir)
    os.remove(root_dir / "LICENSE")
    os.rename(root_dir / new_license, root_dir / "LICENSE")


def update_file_license_info(new_license: str, root_dir: Path):
    replace_in_files(root_dir, "* SPDX-License-Identifier:", "* SPDX-License-Identifier: " + new_license)


def update_copyright(copyright_name: str, root_dir: Path):
    replace_in_files(root_dir, "Copyright (c) [year] [fullname]",
                     f"Copyright (c) {datetime.now().year} {copyright_name}")


def replace_in_files(root_dir: Path, old_text: str, new_text: str):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            with open(os.path.join(root, file), 'r') as f:
                contents = f.read()

            new_contents = contents.replace(old_text, new_text)

            with open(os.path.join(root, file), 'w') as f:
                f.write(new_contents)


def update_license(new_license: str, root_dir: Path, pkg_dir: Path):
    copy_license_file(new_license, root_dir, pkg_dir)
    update_file_license_info(new_license, root_dir)


def ask_for_users_name():
    return input("No user config. Enter your name (i.e. 'Stan Smith')\n>")


def initialise_git(dest_dir: Path):
    original_dir = os.getcwd()
    os.chdir(dest_dir)

    repo = git.Repo.init(os.getcwd())
    repo.git.add(all=True)
    repo.index.commit("Initial commit")

    os.chdir(original_dir)


def copy_all_template_files(args) -> Path:
    src_dir = cpp_start.PKG_DIR_PATH / "templates" / "projects" / "default"
    dest_dir = Path(args.output_directory) / args.proj_name
    shutil.copytree(src_dir, dest_dir)

    # We call this twice because it doesn't catch filenames inside directories that also have their names changed
    # the first time you run it.
    rename_all_the_things(dest_dir, args.proj_name)
    rename_all_the_things(dest_dir, args.proj_name)

    return dest_dir


def main():
    args = cpp_start.get_command_line_parser(license_generator.get_license_paths(cpp_start.LICENSE_TEMPLATES_DIR)).parse_args()
    config = cpp_start.get_config(file_access.FileReadWriter(cpp_start.CONFIG_DIR))
    app = cpp_start.make_cppstart(args, config)

    dest_dir = copy_all_template_files(args)
    os.rename(dest_dir / "template.gitignore", dest_dir / ".gitignore")
    os.chmod(dest_dir / "init.sh", 0o755)
    os.chmod(dest_dir / "build.sh", 0o755)

    update_license(args.license, dest_dir, cpp_start.PKG_DIR_PATH)
    update_copyright(config.get("user", "copyright_name"), dest_dir)

    app.run(file_access.FileReadWriter(Path(args.output_directory)))

    initialise_git(dest_dir)


if __name__ == "__main__":
    main()
