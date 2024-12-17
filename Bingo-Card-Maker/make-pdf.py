#! /usr/bin/python

import argparse
from pathlib import Path
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas

parser = argparse.ArgumentParser()

parser.add_argument('sheets', type=int)

card_dir = Path("./bingo-cards")
card_pathnames = [pathname for pathname in card_dir.glob("*") if pathname.name != ".placeholder"]

def get_size(page_size, orientation):
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

def create_bingo_card_pair(c, img_path_1, img_path_2):
    # 1. Set the position to place the image
    x1 = 75  # X coordinate (left-right)
    x2 = 607.98
    y = 100  # Y coordinate
    
    # 2. Draw the PNG image
    c.drawImage(img_path_1, x1, y)
    c.drawImage(img_path_2, x2, y)

    # 3. Finish Page
    c.showPage()

def create_bingo_card_hex(c, img_path_1, img_path_2, img_path_3, img_path_4, img_path_5, img_path_6):
    # 1. Set the position to place the image
    x_thirdway_point = 355
    y_halfway_point = 374.22
    x1 = 25  # X coordinate (left-right)
    x2 = x1 + x_thirdway_point
    x3 = x2 + x_thirdway_point
    y1 = 25  # Y coordinate
    y2 = 10+ y_halfway_point

    # 2. Draw the PNG image
    c.drawImage(img_path_1, x1, y1) # bottom-left
    c.drawImage(img_path_2, x1, y2) # top-left
    c.drawImage(img_path_3, x2, y1) # bottom-middle
    c.drawImage(img_path_4, x2, y2) # top-middle
    c.drawImage(img_path_5, x3, y1) # bottom-right
    c.drawImage(img_path_6, x3, y2) # top-right

    # 3. Finish Page
    c.showPage()

def create_bingo_card_set(number_of_sheets, cards_per_sheet=6, page_size="PRC8K", orientation="landscape"):
    # 1. get size with applied orientation
    size = get_size(page_size, orientation)

    if cards_per_sheet != 6:
        print("oops, unable to fit that number of cards on a sheet")
        return

    # 2. make canvas and add card images to it
    c = canvas.Canvas("bingo-card-set.pdf", pagesize=size)
    for n in range(1, number_of_sheets):
        try:
            base_index = (6 * n) - 6
            path_1 = card_pathnames[base_index]
            path_2 = card_pathnames[base_index + 1]
            path_3 = card_pathnames[base_index + 2]
            path_4 = card_pathnames[base_index + 3]
            path_5 = card_pathnames[base_index + 4]
            path_6 = card_pathnames[base_index + 5]
            create_bingo_card_hex(c, path_1, path_2, path_3, path_4, path_5, path_6)
        except IndexError as index_error:
            print(index_error)
            break
        except BaseException as e:
            print(e)
            break

    # 3. save
    c.save() 

create_bingo_card_set(parser.parse_args().sheets)
