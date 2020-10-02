#!/usr/bin/env python3.7
# By Apie 2020-10-02
# License: MIT
from functools import partial
from tabulate import tabulate

from scrape_wikipedia_tables import Parser
from util import make_dict

URL = 'https://nl.wikipedia.org/wiki/Douwe_Dabbert'
TABLE_NR = 1
HEADER_START = 1
FIELDS = ('Nummer', 'Titel')

if __name__ == "__main__":
    p = Parser(URL, table_nr=TABLE_NR, header_start=HEADER_START)
    make_d = partial(make_dict, header=p.get_header(), fields=FIELDS)
    print(tabulate(map(make_d, p.get_data()), headers='keys', tablefmt='tsv'))

