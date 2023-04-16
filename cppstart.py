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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("proj_name", help="name of the project")
    parser.add_argument("-d", "--output_directory", help="output directory")

    args = parser.parse_args()

    src_dir = os.path.join("templates", "projects", "default")
    dest_dir = os.path.join(args.output_directory, args.proj_name)
    shutil.copytree(src_dir, dest_dir)

    rename_all_the_things(dest_dir, args.proj_name)
    rename_all_the_things(dest_dir, args.proj_name)

    os.rename(os.path.join(dest_dir, "template.gitignore"), os.path.join(dest_dir, ".gitignore"))


if __name__ == "__main__":
    main()