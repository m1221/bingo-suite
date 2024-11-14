import argparse
import random
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument("-q", "--quantity", help="the number of cards to generate", default=4, type=int)
parser.add_argument("-s", "--source", help="the path to the directory that contains the image icons to be displayed on the bingo cards", default="../source-images/individual-icons", type=str)
parser.add_argument("-o", "--output", help="directory where png cards are saved to", default="./bingo-cards", type=str)
parser.add_argument("-a", "--side_length", help="size of a bingo square, default = 60", default=60, type=int)
parser.add_argument("-p", "--private", help="sets the image icon directory to '../private-source-images/individual-icons'; overrides '--source'.", action=argparse.BooleanOptionalAction)
parser.add_argument("-w", "--words", help="writes words extracted from the image filenames onto the bottoms of the spaces", action=argparse.BooleanOptionalAction)
parser.add_argument("-n", "--numbers", help="if set, uses numbers instead of images; enter the range, eg `-n 1-50`", default="unset", type=str)

if (parser.parse_args().private):
    image_dir = Path("../private-source-images/individual-icons")
else:
    image_dir = Path(parser.parse_args().source)

pathnames = [pathname for pathname in image_dir.glob("[!.]*")]


# utility fn
def getNumbersFromRange(number_range):
    try:
        a, b = number_range.split('-')
        a = int(a)
        b = int(b)
        if b - a >= 24:
            return [i for i in range(a, b + 1)]
        raise(ValueError('The range must span at least 25 numbers.'))
    except BaseException as e:
        print(f'\'{number_range}\' is an invalid range. {e}')
        exit()

# utility fn
def getUserFriendlyName(img_path):
    # '01_spider-web.png' => 'spider web'
    temp = ' '.join(((img_path.name.split('_')[1]).split('.')[0]).split('-'))
    apostrophe_pos = temp.rfind('aaa')
    if apostrophe_pos != -1:
        temp = temp[0:apostrophe_pos] + '\'' + temp[apostrophe_pos + 3]

    hyphen_pos = temp.rfind('hhh')
    if hyphen_pos != -1:
        temp = temp[0:hyphen_pos] + '\'' + temp[hyphen_pos + 3]

    return temp.upper()

def makeBingoCard(image_pathnames, id, side_length=parser.parse_args().side_length, line_thickness=2):
    # 1. Create a blank white image for the bingo card
    header_spacing = 20
    footer_spacing = 15
    card_width = side_length * 5
    card_height = card_width + header_spacing + footer_spacing
    card = Image.new('RGBA', (card_width + line_thickness, card_height), (255, 255, 255, 255))  # White background with full opacity
    draw = ImageDraw.Draw(card)

    # 2. load fonts
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/lyx/dsrom10.ttf", int(side_length / 50) * 10)
        header_font = ImageFont.truetype("/usr/share/fonts/truetype/lyx/dsrom10.ttf", int(side_length / 25) * 10)
        footer_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 10)
        number_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(side_length / 50) * 22)
        space_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(side_length / 50) * 7)
    except IOError:
        font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()
        number_font = ImageFont.load_default()
        space_font = ImageFont.load_default()

    # 3. Draw the Serial Number in the footer
    serial_number = str(id).zfill(3)
    draw.text((2, card_height - footer_spacing + 5), serial_number, fill='black', font=footer_font)

    # 4. Draw the "BINGO" heading
    headers = ["B", "I", "N", "G", "O"]
    for i, letter in enumerate(headers):
        x = i * side_length + (side_length - draw.textsize(letter, font=header_font)[0]) // 2
        draw.text((x, 2), letter, fill='black', font=header_font)

    # 5. draw the images OR  numbers
    number_range = parser.parse_args().numbers
    if number_range == "unset":
        selected_images = random.sample(image_pathnames, 24)  # 25 total minus 1 free space
    else:
        selected_numbers = random.sample(getNumbersFromRange(number_range), 24)

    for i in range(5):
        for j in range(5):
            x = j * side_length
            y = i * side_length + header_spacing  # Adjust for header space

            if i == 2 and j == 2:  # Center space
                draw.rectangle([x, y, x + side_length, y + side_length], fill=(255, 255, 255, 255))
                text = "FREE"
                text_size = draw.textsize(text, font=font)
                draw.text((x + (side_length - text_size[0]) // 2, y + (side_length - text_size[1]) // 2), text, fill='black', font=font)
            else:
                if number_range == "unset":
                    # Get an image and resize it
                    img_path = selected_images.pop()
                    img = Image.open(img_path).convert('RGBA')  # Ensure image has alpha channel
                    img = img.resize((side_length, side_length), Image.ANTIALIAS)

                    # Create a mask for pasting
                    card.paste(img, (x, y), img)  # Use img as the mask to preserve transparency

                    # write descriptive text to the space
                    if (parser.parse_args().words):
                        text = getUserFriendlyName(img_path)
                        text_size = draw.textsize(text, font=space_font)
                        x_pos = x + (side_length - text_size[0]) // 2
                        y_pos = y + (side_length - text_size[1]) * 7 // 8
                        draw.text((x_pos, y_pos), text, fill='black', font=space_font)
                else:
                    number_to_write = str(selected_numbers.pop())
                    text_size = draw.textsize(number_to_write, font=number_font)
                    x_pos = x + (side_length - text_size[0]) // 2
                    y_pos = y + (side_length - text_size[1]) // 2
                    draw.text((x_pos, y_pos), number_to_write, fill='black', font=number_font)

    # 6. Draw grid lines
    for i in range(6):  # 6 lines for 5 squares
        # Vertical lines
        x = i * side_length
        draw.line([(x, header_spacing), (x, card_height - footer_spacing)], fill='black', width=line_thickness)

        # Horizontal lines
        y = i * side_length + header_spacing
        draw.line([(0, y), (card_width, y)], fill='black', width=line_thickness)

    # 7. Save the bingo card to a file
    card.save(f'{parser.parse_args().output}/{serial_number}_bingo-card.png', 'PNG')

for id in range(1, parser.parse_args().quantity + 1):
    makeBingoCard(pathnames, id)