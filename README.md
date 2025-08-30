# Eduranga Downloader

Simple python script to download books from eduranga.pl

## Usage

- Clone this repository

  `git clone https://github.com/jezyq14/eduranga-dl`

- Update `config.json` with your data

  - `book_id` is number that you'll find in your book viewer url (marked as XXX in example below)

    `https://appwsipnet.eduranga.pl/e-podreczniki/podglad/XXX/index.html`

  - `number_of_pages` is just number of pages of the book, can be found at the bottom of book viewer

  - `wsipnet_session` and `wsipnet_session_lifetime` are cookies related to your user

- Run the script

  `python index.py`
