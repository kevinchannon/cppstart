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


def main():
    args = cpp_start.get_command_line_parser(
        license_generator.get_license_paths(cpp_start.LICENSE_TEMPLATES_DIR)).parse_args()
    config = cpp_start.get_config(file_access.FileReadWriter(cpp_start.CONFIG_DIR))

    dest_dir = Path(args.output_directory) / args.proj_name

    app = cpp_start.make_cppstart(args, config)
    app.run(file_access.FileReadWriter(dest_dir))
    app.initialise(dest_dir)


if __name__ == "__main__":
    main()
