import argparse
import shutil
import os
import appdirs
import configparser
import datetime
import git


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


def license_choices():
    license_dir_path = os.path.join("templates", "licenses")
    return [f for f in os.listdir(license_dir_path) if os.path.isfile(os.path.join(license_dir_path, f))]


def copy_license_file(new_license: str, root_dir: str):
    license_path = os.path.join("templates", "licenses", new_license)
    shutil.copy(license_path, root_dir)
    os.remove(os.path.join(root_dir, "LICENSE"))
    os.rename(os.path.join(root_dir, new_license), os.path.join(root_dir, "LICENSE"))


def update_file_license_info(new_license: str, root_dir: str):
    replace_in_files(root_dir, "* SPDX-License-Identifier:", "* SPDX-License-Identifier: " + new_license)


def update_copyright(copyright_name: str, root_dir: str):
    replace_in_files(root_dir, "Copyright (c)", f"Copyright (c) {datetime.datetime.now().year} {copyright_name}")


def replace_in_files(root_dir: str, old_text: str, new_text: str):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            with open(os.path.join(root, file), 'r') as f:
                contents = f.read()

            new_contents = contents.replace(old_text, new_text)

            with open(os.path.join(root, file), 'w') as f:
                f.write(new_contents)


def update_license(new_license: str, root_dir: str):
    copy_license_file(new_license, root_dir)
    update_file_license_info(new_license, root_dir)


def ask_for_users_name():
    return input("No user config. Enter your name (i.e. 'Stan Smith')\n>")


def initialise_git(dest_dir: str):
    original_dir = os.getcwd()
    os.chdir(dest_dir)

    repo = git.Repo.init(os.getcwd())
    repo.git.add(all=True)
    repo.index.commit("Initial commit")

    os.chdir(original_dir)


def main():

    config = configparser.ConfigParser()

    config_dir = appdirs.user_config_dir(appname="cppstart", appauthor=False)
    config_file_path = os.path.join(config_dir, 'config.ini')
    if os.path.isfile(config_file_path):
        config.read(config_file_path)
    else:
        config["user"] = {"copyright_name": ask_for_users_name()}
        os.makedirs(config_dir, exist_ok=True)
        with open(config_file_path, "w") as cfg_file:
            config.write(cfg_file)

    parser = argparse.ArgumentParser()
    parser.add_argument("proj_name", help="name of the project")
    parser.add_argument("-d", "--output_directory", default=".", help="output directory")
    parser.add_argument("-l", "--license", choices=license_choices(), default="MIT",
                        help="the license that will be used in the project")
    parser.add_argument("-c", "--copyright-name", default=config["user"]["copyright_name"],
                        help="name that will be used in copyright info")

    args = parser.parse_args()

    src_dir = os.path.join("templates", "projects", "default")
    dest_dir = os.path.join(args.output_directory, args.proj_name)
    shutil.copytree(src_dir, dest_dir)

    # We call this twice because it doesn't catch filenames inside directories that also have their names changed
    # the first time you run it.
    rename_all_the_things(dest_dir, args.proj_name)
    rename_all_the_things(dest_dir, args.proj_name)

    os.rename(os.path.join(dest_dir, "template.gitignore"), os.path.join(dest_dir, ".gitignore"))

    update_license(args.license, dest_dir)
    update_copyright(args.copyright_name, dest_dir)

    initialise_git(dest_dir)


if __name__ == "__main__":
    main()
