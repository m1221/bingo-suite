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

if (parser.parse_args().private):
    image_dir = Path("../private-source-images/individual-icons")
else:
    image_dir = Path(parser.parse_args().source)

pathnames = [pathname for pathname in image_dir.glob("[!.]*")]

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
    except IOError:
        font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()

    # 3. Draw the Serial Number in the footer
    serial_number = str(id).zfill(3)
    draw.text((2, card_height - footer_spacing + 5), serial_number, fill='black', font=footer_font)

    # 4. Draw the "BINGO" heading
    headers = ["B", "I", "N", "G", "O"]
    for i, letter in enumerate(headers):
        x = i * side_length + (side_length - draw.textsize(letter, font=header_font)[0]) // 2
        draw.text((x, 2), letter, fill='black', font=header_font)

    # 5. draw the images
    selected_images = random.sample(image_pathnames, 24)  # 25 total minus 1 free space

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
                # Get an image and resize it
                img_path = selected_images.pop()
                img = Image.open(img_path).convert('RGBA')  # Ensure image has alpha channel
                img = img.resize((side_length, side_length), Image.ANTIALIAS)

                # Create a mask for pasting
                card.paste(img, (x, y), img)  # Use img as the mask to preserve transparency

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