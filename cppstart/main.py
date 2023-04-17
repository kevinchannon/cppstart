import argparse
import shutil
import os


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
    license_dir_path = os.path.join("../templates", "licenses")
    return [f for f in os.listdir(license_dir_path) if os.path.isfile(os.path.join(license_dir_path, f))]


def copy_license_file(new_license: str, root_dir: str):
    license_path = os.path.join("../templates", "licenses", new_license)
    shutil.copy(license_path, root_dir)
    os.remove(os.path.join(root_dir, "LICENSE"))
    os.rename(os.path.join(root_dir, new_license), os.path.join(root_dir, "LICENSE"))


def update_file_license_info(new_license: str, root_dir: str):
    template_license_text = "* SPDX-License-Identifier:"
    updated_license_text = "* SPDX-License-Identifier: " + new_license
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # Open each file and read its contents
            with open(os.path.join(root, file), 'r') as f:
                contents = f.read()

            new_contents = contents.replace(template_license_text, updated_license_text)

            with open(os.path.join(root, file), 'w') as f:
                f.write(new_contents)


def update_license(new_license: str, root_dir: str):
    copy_license_file(new_license, root_dir)
    update_file_license_info(new_license, root_dir)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("proj_name", help="name of the project")
    parser.add_argument("-d", "--output_directory", default=".", help="output directory")
    parser.add_argument("-l", "--license", choices=license_choices(), default="MIT",
                        help="the license that will be used in the project")

    args = parser.parse_args()

    src_dir = os.path.join("../templates", "projects", "default")
    dest_dir = os.path.join(args.output_directory, args.proj_name)
    shutil.copytree(src_dir, dest_dir)

    # We call this twice because it doesn't catch filenames inside directories that also have their names changed
    # the first time you run it.
    rename_all_the_things(dest_dir, args.proj_name)
    rename_all_the_things(dest_dir, args.proj_name)

    os.rename(os.path.join(dest_dir, "template.gitignore"), os.path.join(dest_dir, "../.gitignore"))

    update_license(args.license, dest_dir)


if __name__ == "__main__":
    main()
