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

parser.add_argument('sheets', type=int,
                    help=("the number of sheets to produce"))
parser.add_argument('spec', type=str,
                    help=(
                    "Select from a page size, orientation, and card/sheet combination"
                    "\n 1 - Letter (216 x 279mm) Landscape, 2 cards per sheet"
                    "\n 2 - Letter (216 x 279mm) Portrait, 1 card per sheet"
                    "\n 3 - ANSI C (432 x 559mm) Landscape, 6 cards per sheet"
                    "\n 4 - A4 (210 x 297mm) Landscape, 2 cards per sheet"
                    "\n 5 - A4 (210 x 297mm) Portrait, 1 card per sheet"
                    "\n 6 - A2 (420 x 594mm) Landscape, 6 pages per sheet"
                    "\n 7 - 4K (390 x 540mm) Landscape, 6 pages per sheet"))
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

MARGIN = 25

def create_sheet_with_1_card(c: canvas, page_width : float, page_height : float, img_path):
    """Makes a page with one bingo cards ('portrait' orientation). """
    card_height = (page_height - MARGIN * 2)
    card_width = (page_width - MARGIN * 2)
    # 1. set the positions to place the images
    x = MARGIN  # X coordinate (left-right)
    y = MARGIN  # Y coordinate

    # 2. draw the PNG image
    c.drawImage(img_path, x, y, card_width, card_height)

    # 3. finish the page
    c.showPage()

def create_sheet_with_2_cards(c: canvas, page_width : float, page_height : float, *img_paths):
    """Makes a page with two bingo cards ('landscape' orientation). """
    card_height = (page_height - MARGIN * 2)
    card_width = (page_width - MARGIN * 4) / 2
    # 1. set the positions to place the images
    x1 = MARGIN  # X coordinate (left-right)
    x2 = x1 + card_width + MARGIN * 2 
    y = MARGIN  # Y coordinate

    # 2. draw the PNG image
    c.drawImage(img_paths[0], x1, y, card_width, card_height)
    c.drawImage(img_paths[1], x2, y, card_width, card_height)

    # 3. finish the page
    c.showPage()


def create_sheet_with_6_cards(c : canvas, page_width : float, page_height : float, *img_paths):
    """Makes a page with 6 bingo cards ('landscape' orientation). """
    card_height = (page_height - MARGIN * 4) / 2
    card_width = (page_width - MARGIN * 6) / 3
    # 1. Set the position to place the image
    x1 = MARGIN  # X coordinate (left-right)
    x2 = x1 + card_width + MARGIN * 2
    x3 = x2 + card_width + MARGIN * 2
    y1 = MARGIN  # Y coordinate
    y2 = y1 + card_height + MARGIN * 2

    # 2. Draw the PNG image
    c.drawImage(img_paths[0], x1, y1, card_width, card_height)  # bottom-left
    c.drawImage(img_paths[1], x1, y2, card_width, card_height)  # top-left
    c.drawImage(img_paths[2], x2, y1, card_width, card_height)  # bottom-middle
    c.drawImage(img_paths[3], x2, y2, card_width, card_height)  # top-middle
    c.drawImage(img_paths[4], x3, y1, card_width, card_height)  # bottom-right
    c.drawImage(img_paths[5], x3, y2, card_width, card_height)  # top-right

    # 3. Finish Page
    c.showPage()


def create_card_set(num_sheets : int, specification : str = "0") -> None:
    """
    """
    # CONVERSION FACTOR
    CF = 72 / 25.4  # convert from mm to reportlab unit

    create_card = create_sheet_with_6_cards

    match specification:
        case "1":
            page_size = pagesizes.letter
            page_size = pagesizes.landscape(page_size)
            cards_per_sheet = 2
            create_card = create_sheet_with_2_cards
        case "2":
            page_size = pagesizes.letter
            page_size = pagesizes.portrait(page_size)
            cards_per_sheet = 1
            create_card = create_sheet_with_1_card
        case "3":
            # ANSI C Size
            page_size = (432 * CF, 559 * CF)
            page_size = pagesizes.landscape(page_size)
            cards_per_sheet = 6
            create_card = create_sheet_with_6_cards
        case "4":
            page_size = pagesizes.A4
            page_size = pagesizes.landscape(page_size)
            cards_per_sheet = 2
            create_card = create_sheet_with_2_cards
        case "5":
            page_size = pagesizes.A4
            page_size = pagesizes.portrait(page_size)
            cards_per_sheet = 1
            create_card = create_sheet_with_1_card
        case "6":
            page_size = pagesizes.A2
            page_size = pagesizes.landscape(page_size)
            cards_per_sheet = 6
            create_card = create_sheet_with_6_cards
        case "7":
            # 4K (large paper commonly used in Chinese schools)
            page_size = (390 * CF, 549 * CF)
            page_size = pagesizes.landscape(page_size)
            cards_per_sheet = 6
            create_card = create_sheet_with_6_cards
        case _:
            raise ValueError(f"'{specification}' not recognized. Please enter a valid selection.")

    num_sheets_saved = 0
    error_status = 0  # use for error recording

    # 2. make canvas and add card images to it
    c = canvas.Canvas(str(SAVE_PATH), pagesize=page_size)
    for n in range(0, num_sheets):
        try:  # use try-block so that a pdf is saved regardless of any errors
            base_index = n * cards_per_sheet
            paths = [card_pathnames[base_index + i] for i in range(cards_per_sheet)]
            create_card(c, page_size[0], page_size[1], *tuple(paths))
            num_sheets_saved += 1
        except IndexError as index_error:
            error_status = index_error
            break
        except BaseException as e:
            error_status = e
            break

    # 3. save
    c.save()

    print("*** SUMMARY ***")
    print(f"Number of sheets saved: {num_sheets_saved}")
    print(f"Cards per sheet: {cards_per_sheet}")
    print(f"Location: {SAVE_PATH}")
    if error_status != 0:
        raise error_status


create_card_set(parser.parse_args().sheets, parser.parse_args().spec)
