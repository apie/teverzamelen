#!/usr/bin/env python3
# By Apie 2020-10-02
# License: MIT
from functools import partial
from tabulate import tabulate

from scrape_wikipedia_tables import Parser
from util import make_dict

URL = 'https://nl.wikipedia.org/wiki/Vierkleurenreeks'
HEADER_START = 1
FIELDS = ('Nummer', 'Titel')


if __name__ == "__main__":
    p = Parser(URL, header_start=HEADER_START)
    make_d = partial(make_dict, header=p.get_header(), fields=FIELDS)
    print(tabulate(map(make_d, p.get_data()), headers='keys', tablefmt='tsv'))

