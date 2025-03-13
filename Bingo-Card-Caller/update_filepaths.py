#! /usr/bin/python3
"""
The purpose of this script is to update the './code/filepaths.js' file used
by the Bingo Caller browser app. the filepaths.js file contains an array of
filepaths (type: String) that link to the Bingo images.

This script:
    1. gets paths from a directory and writes them to ./code/filepaths.js
        (default: PROJECT_ROOT/source-images/individual-icons)
    2. MUST BE RUN from project root. Examples:
        $ ./Bingo-Card-Caller/update_filespaths.py
        $ ./Bingo-Card-Caller/update_filespaths.py --help
        $ ./Bingo-Card-Caller/update_filespaths.py --source "./target_dir"

"""

from pathlib import Path
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("-s", "--source", help=(
                    "the path of the directory that contains the image icons "
                    "to be displayed on the bingo cards; it must a descendant "
                    "of the project root directory"), type=str)


def __get_source_dir__() -> Path:
    """Get a directory"""
    user_path = parser.parse_args().source
    default_path = "./source-images/individual-icons"
    source_dir = Path(default_path if user_path is None else user_path)

    if not source_dir.exists():
        raise FileExistsError(f"ERROR: '{source_dir}' does not exist.")

    return source_dir


with open("./Bingo-Card-Caller/code/filepaths.js", mode="w",
          encoding="utf-8") as outfile:
    # gather filepaths
    raw_paths = list(__get_source_dir__().glob("[!.]*"))

    # compose the string to be written
    WRITE_OUT = "let filepaths = ["

    for path in raw_paths:
        WRITE_OUT += "\n    '../../" + str(path) + "',"
        # the root directory is located 2 levels up from filepaths.js

    WRITE_OUT = WRITE_OUT[:-1]  # clip the last comma
    WRITE_OUT += "\n];\n"  # close the variable

    # finish
    outfile.write(WRITE_OUT)
    print(f"***Successfully wrote to '{outfile.name}'.***")
