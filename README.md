# About Bingo Suite

Make Bingo card PDFs and play bingo with the browser app.

Bingo Suite includes three scripts:
1. update-filepaths.py
  * updates Bingo-Card-Caller/code/filepaths.js for the browser app (bingo-caller.html)
1. make_cards.py
  * makes bingo cards from png files or from a user-defined number range
1. make_pdf.py
  * gathers bingo cards and prints them to pdf

This app suite is still heavily under construction. See TODO.txt for more information.

# Dependencies

Python 3.12.0 and the following libraries (which you can install with pip):

* PIL
    * `pip install pillow`
* reportlab
    * `pip install reportLab`