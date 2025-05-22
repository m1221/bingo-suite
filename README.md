# About Bingo Suite

Make Bingo card PDFs and play bingo with the browser app.

Bingo Suite includes three scripts:

1. `update_filepaths.py`
  * updates Bingo-Card-Caller/code/filepaths.js for the browser app (bingo-caller.html)
  * <img src="doc-images/screenshot_update_filepaths.jpg" width="600px">

2. `make_cards.py`
  * makes bingo cards from png files OR from a user-defined number range
  * <img src="doc-images/screenshot_make_cards.jpg" width="600px">

3. `make_pdf.py`
  * gathers bingo cards and prints them to pdf
  * <img src="doc-images/screenshot_make_pdf.jpg" width="600px">


# Dependencies

Best practice is to use Python virtual environments.

After establishing and activating a virtual environment of your choice, you can install the required dependencies via pip.
```
pip install -r requirements.txt
```

# Examples

## Making a Card
```bash
# `python3 make_cards.py -h` for help
# python3 make_cards.py number_of_cards
$ python3 make_cards.py 1  # produce a single card
```

<img src="doc-images/screenshot_sample_card.jpg" width="auto" height="300px">

## Make a Sheet

```bash
# `python3 make_pdf.py -h` for help
# python3 make_pdf.py number_of_sheets form_factor
$ python3 make_pdf.py 1 1
```
<img src="doc-images/screenshot_sample_sheet.jpg" width="auto" height="300px">

## Using the Card Caller

Run `Bingo_Card-Caller/update_filepaths.py` to update the filepaths that will be used by the browser app.

Open the browser app at `Bingo_Card-Caller/code/bingo-caller.html`

<img src="doc-images/screenshot_browser.jpg" width="auto" height="400px">