#! /usr/bin/python3
"""
Make Cards

This script makes 5x5 bingo cards (png format) from either local images or a
user-specified number range.

For usage information:
$ python3 Bingo-Card-Maker/make_cards.py -h
"""

from pathlib import Path
import argparse
import random
import sys
from PIL import Image, ImageDraw, ImageFont


def __clamp_inner_image_scale__(arg: str) -> float:
    """Sanitize and then clamp image-in-box scale to [0.5, 1.0]."""
    try:
        f = float(arg)
    except BaseException as e:
        print(e)
        raise argparse.ArgumentTypeError(f"'{arg}' of type {type(arg)} \
                                        cannot be converted into a float.")

    if f < 0.5:
        print(f"--inner_image_scale clamped from {f} to 0.5")
        return 0.5
    if f > 1.0:
        print(f"--inner_image_scale clamped from {f} to 1.0")
        return 1.0
    return f


parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)


parser.add_argument("quantity", type=int,
                    help="the number of cards to generate")
parser.add_argument("-S", "--single_pool", help=(
                    "if set, items are pulled from a single pool\nby "
                    "default, items are pulled from MULTIPLE POOLS"
                    "(one pool for each letter of 'BINGO')"),
                    action=argparse.BooleanOptionalAction)
parser.add_argument("-s", "--source", help=(
                    "the path of the dir that contains the image icons "
                    "for the cards, relative to 'BingoSuite'."
                    "\nThe default is 'source-images/individual-icons'"),
                    default="source-images/individual-icons", type=str)
parser.add_argument("-o", "--output", help=(
                    "the directory to which png cards are saved, relative to "
                    "'Bingo-Card-Maker'\nthe default is 'bingo-cards'"),
                    default="bingo-cards", type=str)
parser.add_argument("-a", "--side_length",
                    help="size of a bingo square\ndefault = 60",
                    default=60, type=int)
parser.add_argument("-i", "--inner_image_scale", help=(
                    "the percent of a bingo space that the image should "
                    "fill; clamped from 0.5 to 1.0\ndefault = 1.0"),
                    default=1.0, type=__clamp_inner_image_scale__)
parser.add_argument("-w", "--words", help=(
                    "writes words extracted from the image filenames onto "
                    "the bottoms of the bingo spaces\nby default, no words " 
                    "appear on bingo spaces"),
                    action=argparse.BooleanOptionalAction)
parser.add_argument("-n", "--number_range", help=(
                    "if set, uses numbers instead of images\nenter a range: "
                    "eg `-n 1-50`"), type=str)
parser.add_argument("-Q", "--quiet_mode", help=(
                    "if set, silence the completion message at the end of "
                    "the script"), action=argparse.BooleanOptionalAction)

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args_in = parser.parse_args()
script_dir = Path(__file__).resolve().parent
SAVE_DIR = script_dir / args_in.output

if not SAVE_DIR.exists(follow_symlinks=False):
    raise FileExistsError(f"The directory '{SAVE_DIR}' could not be found.")


def __load_font__(font_dir: str, font_size: int):
    """A wrapper for loading fonts without crashing the script."""
    try:
        return ImageFont.truetype(font_dir, font_size)
    except BaseException as e:
        print(e)
        return ImageFont.load_default()


# utility fn
def __make_list_from_range__(number_range: str) -> list[str]:
    """Check user-input and return a list spanning the specified range.
    
    Parameters
    ----------
    number_range : str
        format should be "a-b", where b-a >= 24
    """
    a, b = number_range.split('-')
    a = int(a)
    b = int(b)
    if b - a >= 24:
        return [str(i) for i in range(a, b + 1)]
    raise ValueError(f"ERROR: '{number_range}' is invalid. The difference "
                     "between the max and min values must be at least 24.")


# utility fn
def __get_display_name__(img_path: str) -> str:
    """Transforms certain sequences in filepaths into special characters.
    
    Supported Sequences:
        aaa -> ' [apostrophe]
        hhh -> - [hyphen]
    """
    temp = ' '.join(((img_path.name).split('.')[0]).split('-'))
    apostrophe_pos = temp.rfind('aaa')
    if apostrophe_pos != -1:
        temp = temp[0:apostrophe_pos] + '\'' + temp[apostrophe_pos + 3:]

    hyphen_pos = temp.rfind('hhh')
    if hyphen_pos != -1:
        temp = temp[0:hyphen_pos] + '-' + temp[hyphen_pos + 3:]

    return temp[:16].upper()  # truncate after x characters


def make_card(card_id: int, side_length: int = args_in.side_length,
                  line_thickness: int = 2):
    """Makes a png file according to user specifications.
    
    Parameters
    ----------
    card_id :
        the number printed on the bottom left-hand corner of the card
    side_length :
        the length of a bingo square (presumably in millimeters?)
    line_thickness :
        the thickness of the grid lines
    """
    # 1. Create a blank white image for the bingo card
    header_spacing = 20
    footer_spacing = 15
    card_width = side_length * 5
    card_height = card_width + header_spacing + footer_spacing
    # White background with full opacity
    card = Image.new('RGBA', (card_width + line_thickness, card_height),
                     (255, 255, 255, 255))
    draw = ImageDraw.Draw(card)

    # 2. load fonts
    size_mod = int(side_length / 50)
    font_prefix = "/usr/share/fonts/truetype/"
    font = __load_font__(font_prefix + "lyx/dsrom10.ttf", size_mod * 10)
    header_font = __load_font__(font_prefix + "lyx/dsrom10.ttf", size_mod * 20)
    footer_font = __load_font__(font_prefix + "dejavu/DejaVuSerif.ttf", 10)
    number_font = __load_font__(font_prefix + "dejavu/DejaVuSans.ttf", size_mod * 22)
    box_font = __load_font__(font_prefix + "dejavu/DejaVuSans.ttf", size_mod * 8)
    box_font_small = __load_font__(font_prefix + "dejavu/DejaVuSans.ttf", size_mod * 6)

    # 3. Draw the Serial Number in the footer
    serial_number = str(card_id).zfill(3)
    draw.text((2, card_height - footer_spacing + 5), serial_number, fill='black', font=footer_font)

    # 4. Draw the "BINGO" heading
    headers = ["B", "I", "N", "G", "O"]
    for i, letter in enumerate(headers):
        x = i * side_length + (side_length - draw.textlength(letter, font=header_font)[0]) // 2
        draw.text((x, 2), letter, fill='black', font=header_font)

    # 5. make selection pools
    number_range = args_in.number_range

    # 5.A check if should use one pool
    if args_in.single_pool:
        if number_range:
            selection_pool = random.sample(__make_list_from_range__(number_range), 25)
        else:
            selection_pool = random.sample(image_pathnames, 25)
    else:  # 5.B use multiple pools
        pools = {}
        if number_range:
            numbers = __make_list_from_range__(number_range)

        for i in range(5):
            pools[i] = random.sample(numbers, 5) if number_range \
                else random.sample(image_pathnames, 5)

        selection_pool = ['0'] * 25
        for k in range(25):
            source_index = k % 5
            selection_pool[k] = pools[source_index].pop()

    # 6. draw the images OR numbers
    for i in range(5):
        for j in range(5):
            x = j * side_length
            y = i * side_length + header_spacing  # Adjust for header space

            if i == 2 and j == 2:  # Center space
                selection_pool.pop()
                draw.rectangle([x, y, x + side_length, y + side_length],
                               fill=(255, 255, 255, 255))
                text = "FREE"
                text_size = draw.textlength(text, font=font)
                draw.text((x + (side_length - text_size[0]) // 2,
                           y + (side_length - text_size[1]) // 2),
                           text, fill='black', font=font)
                continue

            if number_range:
                number_to_write = selection_pool.pop()
                text_size = draw.textlength(number_to_write, font=number_font)
                x_pos = x + (side_length - text_size[0]) // 2
                y_pos = y + (side_length - text_size[1]) // 2
                draw.text((x_pos, y_pos), number_to_write, fill='black',
                          font=number_font)
            else:
                # Get an image and resize it
                img_path = selection_pool.pop()
                # Ensure image has alpha channel
                img = Image.open(img_path).convert('RGBA')
                scale_factor = args_in.inner_image_scale
                scaled_length = round(side_length * scale_factor)
                img = img.resize((scaled_length, scaled_length),
                                 Image.ANTIALIAS)

                # Create a mask for pasting
                offset = round(side_length * (1 - scale_factor) / 2)
                # Use img as the mask to preserve transparency
                card.paste(img, (x + offset, y + offset), img)

                # write descriptive text to the space
                if args_in.words:
                    text = __get_display_name__(img_path)
                    text_font = box_font_small if len(text) > 10 else box_font
                    text_size = draw.textlength(text, font=text_font)
                    x_pos = x + (side_length - text_size[0]) // 2
                    y_pos = y + (side_length - text_size[1]) * 19 // 20
                    draw.text((x_pos, y_pos), text, fill='black', font=text_font)

    # 7. Draw grid lines
    for i in range(6):  # 6 lines for 5 squares
        # Vertical lines
        x = i * side_length
        draw.line([(x, header_spacing), (x, card_height - footer_spacing)],
                  fill='black', width=line_thickness)

        # Horizontal lines
        y = i * side_length + header_spacing
        draw.line([(0, y), (card_width, y)], fill='black',
                  width=line_thickness)

    # 8. Save the bingo card to a file
    card.save(f'{SAVE_DIR}/{serial_number}_bingo-card.png', 'PNG')


def __print_termination_message__(success: bool = True):
    """Upon script termination, display user specifications."""
    result = "SUCCESS" if success else "FAILURE"
    make_mode = "Numbers" if args_in.number_range else "Images"
    range_or_source_h = "Range" if args_in.number_range else "Source Directory"
    range_or_source = args_in.number_range if args_in.number_range else args_in.source
    print(f"*** {result}! ***")
    if success:
        print(f"You created {args_in.quantity} cards in the "
              f"'{args_in.output}' directory.")
    print(f"""SPECIFICATIONS:
  Type: {make_mode}
  {range_or_source_h}: {range_or_source}
  Pool(s): {"Single" if args_in.single_pool else "Multiple"}
  Write Words on Cards: {"Yes" if args_in.words else "No"}
  Side Length: {args_in.side_length}
  Inner Image Scale (only applies to images): {args_in.inner_image_scale}
""")


try:
    if args_in.number_range is None:
        image_dir = script_dir.parent / args_in.source
        image_pathnames = list(image_dir.glob("[!.]*"))

    for serial_id in range(1, args_in.quantity + 1):
        make_card(serial_id)

    if not args_in.quiet_mode:
        __print_termination_message__()
except Exception as e:
    __print_termination_message__(success=False)
    if args_in.quiet_mode:
        print("Error: ", e)
    else:
        print("Full Error Message:")
        raise(e)
