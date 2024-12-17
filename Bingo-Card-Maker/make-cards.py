#! /usr/bin/python

import argparse
import random
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def __clamp_inner_image_scale__(arg):
    try:
        f = float(arg)
    except:
        raise argparse.ArgumentTypeError(f"'{arg}' of type {type(arg)} cannot be converted into a float.")
    
    if f < 0.5:
        print(f"--inner_image_scale clamped from {f} to 0.5")
        return 0.5
    elif f > 1.0:
        print(f"--inner_image_scale clamped from {f} to 1.0")
        return 1.0
    return f

parser = argparse.ArgumentParser()

parser.add_argument("-q", "--quantity", help="the number of cards to generate", default=4, type=int)
parser.add_argument("-S", "--single_pool", help="if set, items are pulled from a single pool; by default, items are pulled from pools - one pool for each letter of 'BINGO'", action=argparse.BooleanOptionalAction)
parser.add_argument("-s", "--source", help="the path of the directory that contains the image icons to be displayed on the bingo cards", default="../source-images/individual-icons", type=str)
parser.add_argument("-o", "--output", help="directory where png cards are saved to; the default directory is './bingo-cards'", default="./bingo-cards", type=str)
parser.add_argument("-a", "--side_length", help="size of a bingo square, default = 60", default=60, type=int)
parser.add_argument("-i", "--inner_image_scale", help="what percent of a bingo space should the image fill; clamped from 0.5 to 1.0; default = 1.0", default=1.0, type=__clamp_inner_image_scale__)
parser.add_argument("-w", "--words", help="writes words extracted from the image filenames onto the bottoms of the bingo spaces; by default, no words appear on bingo spaces", action=argparse.BooleanOptionalAction)
parser.add_argument("-n", "--number_range", help="if set, uses numbers instead of images; enter the range, eg `-n 1-50`", type=str)
parser.add_argument("-Q", "--quiet_mode", help="if set, silence the completion message at the end of the script", action=argparse.BooleanOptionalAction)

def __loadFont__(dir, font_size):
    try:
        return ImageFont.truetype(dir, font_size)
    except:
        return ImageFont.load_default()

# utility fn
def __getNumberListFromUserInput__(number_range):
    try:
        a, b = number_range.split('-')
        a = int(a)
        b = int(b)
        if b - a >= 24:
            return [str(i) for i in range(a, b + 1)]
        raise(ValueError('The range must span at least 25 numbers.'))
    except BaseException as e:
        print(f'\'{number_range}\' is an invalid range. {e}')
        exit()

# utility fn
def __getDisplayName__(img_path):
    temp = ' '.join(((img_path.name).split('.')[0]).split('-'))
    apostrophe_pos = temp.rfind('aaa')
    if apostrophe_pos != -1:
        temp = temp[0:apostrophe_pos] + '\'' + temp[apostrophe_pos + 3:]

    hyphen_pos = temp.rfind('hhh')
    if hyphen_pos != -1:
        temp = temp[0:hyphen_pos] + '-' + temp[hyphen_pos + 3:]

    return temp[:16].upper() # truncate after x characters

def makeBingoCard(id, side_length=parser.parse_args().side_length, line_thickness=2):
    # 1. Create a blank white image for the bingo card
    header_spacing = 20
    footer_spacing = 15
    card_width = side_length * 5
    card_height = card_width + header_spacing + footer_spacing
    card = Image.new('RGBA', (card_width + line_thickness, card_height), (255, 255, 255, 255))  # White background with full opacity
    draw = ImageDraw.Draw(card)

    # 2. load fonts
    size_mod = int(side_length / 50)
    font_prefix = "/usr/share/fonts/truetype/"
    font = __loadFont__(font_prefix + "lyx/dsrom10.ttf", size_mod * 10)
    header_font = __loadFont__(font_prefix + "lyx/dsrom10.ttf", size_mod * 20)
    footer_font = __loadFont__(font_prefix + "dejavu/DejaVuSerif.ttf", 10)
    number_font = __loadFont__(font_prefix + "dejavu/DejaVuSans.ttf", size_mod * 22)
    box_font = __loadFont__(font_prefix + "dejavu/DejaVuSans.ttf", size_mod * 8)
    box_font_small = __loadFont__(font_prefix + "dejavu/DejaVuSans.ttf", size_mod * 6)

    # 3. Draw the Serial Number in the footer
    serial_number = str(id).zfill(3)
    draw.text((2, card_height - footer_spacing + 5), serial_number, fill='black', font=footer_font)

    # 4. Draw the "BINGO" heading
    headers = ["B", "I", "N", "G", "O"]
    for i, letter in enumerate(headers):
        x = i * side_length + (side_length - draw.textsize(letter, font=header_font)[0]) // 2
        draw.text((x, 2), letter, fill='black', font=header_font)

    # 5. make selection pools
    number_range = parser.parse_args().number_range

    # 5.A check if should use one pool
    if parser.parse_args().single_pool:
        if number_range:
            selection_pool = random.sample(__getNumberListFromUserInput__(number_range), 25)
        else:
            selection_pool = random.sample(image_pathnames, 25)
    else: #5.B use multiple pools
        pools = {}
        if number_range:
            numbers = __getNumberListFromUserInput__(number_range)

        for i in range(5):
            pools[i] = random.sample(numbers, 5) if number_range else random.sample(image_pathnames, 5)
     
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
                draw.rectangle([x, y, x + side_length, y + side_length], fill=(255, 255, 255, 255))
                text = "FREE"
                text_size = draw.textsize(text, font=font)
                draw.text((x + (side_length - text_size[0]) // 2, y + (side_length - text_size[1]) // 2), text, fill='black', font=font)
                continue

            if number_range:
                number_to_write = selection_pool.pop()
                text_size = draw.textsize(number_to_write, font=number_font)
                x_pos = x + (side_length - text_size[0]) // 2
                y_pos = y + (side_length - text_size[1]) // 2
                draw.text((x_pos, y_pos), number_to_write, fill='black', font=number_font)
            else:
                # Get an image and resize it
                img_path = selection_pool.pop()
                img = Image.open(img_path).convert('RGBA')  # Ensure image has alpha channel
                scale_factor = parser.parse_args().inner_image_scale
                scaled_length = round(side_length * scale_factor)
                img = img.resize((scaled_length, scaled_length), Image.ANTIALIAS)

                # Create a mask for pasting
                offset = round(side_length * (1 - scale_factor) / 2)
                card.paste(img, (x + offset, y + offset), img)  # Use img as the mask to preserve transparency

                # write descriptive text to the space
                if (parser.parse_args().words):
                    text = __getDisplayName__(img_path)
                    text_font = box_font_small if len(text) > 10 else box_font
                    text_size = draw.textsize(text, font=text_font)
                    x_pos = x + (side_length - text_size[0]) // 2
                    y_pos = y + (side_length - text_size[1]) * 19 // 20
                    draw.text((x_pos, y_pos), text, fill='black', font=text_font)

    # 7. Draw grid lines
    for i in range(6):  # 6 lines for 5 squares
        # Vertical lines
        x = i * side_length
        draw.line([(x, header_spacing), (x, card_height - footer_spacing)], fill='black', width=line_thickness)

        # Horizontal lines
        y = i * side_length + header_spacing
        draw.line([(0, y), (card_width, y)], fill='black', width=line_thickness)

    # 8. Save the bingo card to a file
    card.save(f'{parser.parse_args().output}/{serial_number}_bingo-card.png', 'PNG')

if parser.parse_args().number_range == None:
    image_dir = Path(parser.parse_args().source)
    image_pathnames = [pathname for pathname in image_dir.glob("[!.]*")]

for id in range(1, parser.parse_args().quantity + 1):
    makeBingoCard(id)

if not parser.parse_args().quiet_mode:
    print(f"""*** Success! You created {parser.parse_args().quantity} cards in '{parser.parse_args().output}' directory.***
  Type: {"Numbers" if parser.parse_args().number_range else "Images"}
  {"Range" if parser.parse_args().number_range else "Source"}: {parser.parse_args().number_range if parser.parse_args().number_range else parser.parse_args().source}
  Pool: {"Single" if parser.parse_args().single_pool else "Multi"}
  Write Words on Cards: {"Yes" if parser.parse_args().words else "No"}
  Side Length: {parser.parse_args().side_length}
  Inner Image Scale (only applies to images): {parser.parse_args().inner_image_scale}
""")