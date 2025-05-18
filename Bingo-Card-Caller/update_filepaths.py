#! /usr/bin/python3
"""
The purpose of this script is to update 'Bingo-Card-Caller/code/filepaths.js' The filepaths.js file contains an array of filepaths (type: String)
that link to the Bingo images.

To learn more, run:
$ python3 Bingo-Card-Caller/update_filepaths.py

"""

from pathlib import Path
import argparse
import sys


parser = argparse.ArgumentParser()

parser.add_argument("-s", "--source", help=(
                    "the name of the directory that contains the image icons, "
                    "relative to 'BingoSuite`; the default is "
                    "'source-images/individual-icons'"),
                    default="source-images/individual-icons", type=str)

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

project_root = Path(__file__).resolve().parent.parent
img_dir = project_root / parser.parse_args().source
if not img_dir.exists(follow_symlinks=False):
    raise FileNotFoundError(f"The directory '{img_dir}' does not exist.")

with open(project_root / "Bingo-Card-Caller/code/filepaths.js", mode="w",
          encoding="utf-8") as outfile:
    # gather filepaths
    raw_paths = list(img_dir.glob("[!.]*"))

    # compose the string to be written
    WRITE_OUT = "let filepaths = ["

    for path in raw_paths:
        temp_string = str(path)
        pos = temp_string.find('BingoSuite')
        WRITE_OUT += "\n    '../.." + temp_string[pos + 10:] + "',"
        # the root directory is located 2 levels up from filepaths.js

    WRITE_OUT = WRITE_OUT[:-1]  # clip the last comma
    WRITE_OUT += "\n];\n"  # close the variable

    # finish
    outfile.write(WRITE_OUT)
    print(f"***Successfully wrote to '{outfile.name}'.***")
