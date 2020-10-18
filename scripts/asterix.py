#!/usr/bin/env python3
# By Apie 2020-10-02
# License: MIT
from itertools import filterfalse
from functools import partial
from tabulate import tabulate

from util import make_dict
from scrape_wikipedia_tables import Parser

URL = 'https://nl.wikipedia.org/wiki/Lijst_van_albums_van_Asterix'
FIELDS = ('Nr.', 'Nederlandse titel')  # Cleaned first column name


def clean_first_column(row):
    row[0] = row[0].split()[0]
    return row


if __name__ == "__main__":
    p = Parser(URL)
    # Cleanup first header column
    data_header = clean_first_column(p.get_header())
    data_list = map(
        # Clean up first column
        clean_first_column,
        # Remove rows that are not albums
        filterfalse(
            lambda i: i[0].startswith('scenario'),
            p.get_data()
        )
    )
    make_d = partial(make_dict, header=data_header, fields=FIELDS)
    print(tabulate(map(make_d, data_list), headers='keys', tablefmt='tsv'))

