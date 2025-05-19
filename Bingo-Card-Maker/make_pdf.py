#! /usr/bin/python3
"""
Make PDF

This script uses the png files found in `Bingo-Card-Maker/bingo-cards` to 
generate a pdf file of x sheets (user-specified number).

For more information, run:
$ python3 Bingo-Card-Maker/make_pdf.py -h

"""

import argparse
import sys
from pathlib import Path
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-s", "--source", help=(
                    "the name of the directory that contains the cards, "
                    "relative to 'Bingo-Card-Maker'\nthe default value "
                    "is 'bingo-cards'."),
                    default="bingo-cards", type=str)
parser.add_argument("-o", "--output", help=(
                    "the name of the output pdf file containing the cards \n"
                    "the default value is 'bingo-card-set.pdf'; "
                    "it is placed in the 'Bingo-Card-Maker' directory"),
                    default="bingo-card-set.pdf", type=str)
parser.add_argument('sheets', type=int,
                    help=("the number of sheets to produce"))

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

parent_dir = Path(__file__).resolve().parent
SAVE_PATH = parent_dir / parser.parse_args().output

card_dir = parent_dir / parser.parse_args().source
if not card_dir.exists(follow_symlinks=False):
    raise FileNotFoundError(f"The directory '{card_dir}' does not exist.")

card_pathnames = [pathname for pathname in card_dir.glob("*")
                  if pathname.name != ".placeholder"]


def get_paper_size(page_size: str, orientation: str) -> tuple[float]:
    """Returns the dimensions of the paper (H, W) in millimeters.

    Parameters
    ----------
    page_size : str
        supports "prc8k", "letter", and "a4"
    orientation : str
        supports "landscape" and "portrait"
    """
    # 1. Sanitize arguments
    page_size = page_size.lower()
    orientation = orientation.lower()

    # 2. get dimensions
    if page_size == "prc8k":
        size = (748.44, 1065.96)
    elif page_size == "letter":
        size = pagesizes.letter
    elif page_size == "a4":
        size = pagesizes.A4
    else:
        raise ValueError("Unsupported page size. Use 'letter', 'a4', or 'prc8k'.")

    # 3. Adjust orientation
    if orientation == "landscape":
        size = pagesizes.landscape(size)
    elif orientation == "portrait":
        size = pagesizes.portrait(size)
    else:
        raise ValueError("Unsupported orientation. Use 'landscape' or 'portrait'.")
    return size


def create_card_pair(canvas_in: canvas, img_path_1: str, img_path_2: str):
    """Makes a page with two bingo cards."""
    # 1. set the positions to place the images
    x1 = 75  # X coordinate (left-right)
    x2 = 607.98
    y = 100  # Y coordinate

    # 2. draw the PNG image
    canvas_in.drawImage(img_path_1, x1, y)
    canvas_in.drawImage(img_path_2, x2, y)

    # 3. finish the page
    canvas_in.showPage()


def create_card_hex(c, *img_paths):
    """Makes a page with 6 bingo cards."""
    # 1. Set the position to place the image
    x_thirdway_point = 355
    y_halfway_point = 374.22
    x1 = 25  # X coordinate (left-right)
    x2 = x1 + x_thirdway_point
    x3 = x2 + x_thirdway_point
    y1 = 25  # Y coordinate
    y2 = 10 + y_halfway_point

    # 2. Draw the PNG image
    c.drawImage(img_paths[0], x1, y1)  # bottom-left
    c.drawImage(img_paths[1], x1, y2)  # top-left
    c.drawImage(img_paths[2], x2, y1)  # bottom-middle
    c.drawImage(img_paths[3], x2, y2)  # top-middle
    c.drawImage(img_paths[4], x3, y1)  # bottom-right
    c.drawImage(img_paths[5], x3, y2)  # top-right

    # 3. Finish Page
    c.showPage()


def create_card_set(number_of_sheets, cards_per_sheet=6,
                    page_size="PRC8K", orientation="landscape"):
    """Makes a pdf according to the argument specifications."""

    num_sheets_saved = 0
    error_status = 0  # use for error recording

    # 1. get size with applied orientation
    size = get_paper_size(page_size, orientation)

    if cards_per_sheet != 6:
        print("oops, unable to fit that number of cards on a sheet")
        return

    # 2. make canvas and add card images to it
    c = canvas.Canvas(str(SAVE_PATH), pagesize=size)
    for n in range(0, number_of_sheets):
        try:  # use try-block so that a pdf is saved regardless of any errors
            paths = [""] * 6
            base_index = 6 * n
            paths[0] = card_pathnames[base_index]
            paths[1] = card_pathnames[base_index + 1]
            paths[2] = card_pathnames[base_index + 2]
            paths[3] = card_pathnames[base_index + 3]
            paths[4] = card_pathnames[base_index + 4]
            paths[5] = card_pathnames[base_index + 5]
            create_card_hex(c, *tuple(paths))
            num_sheets_saved += 1
        except IndexError as index_error:
            error_status = index_error
            break
        except BaseException as e:
            error_status = e
            break

    # 3. save
    c.save()

    print(f"***SUMMARY: {num_sheets_saved} sheets saved to `{SAVE_PATH}`.***")
    if error_status != 0:
        raise error_status


create_card_set(parser.parse_args().sheets)
