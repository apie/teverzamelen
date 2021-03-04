#!/usr/bin/env python3
# By Apie 2021-03-04
# License: MIT
import requests
from functools import partial
from tabulate import tabulate

from lxml import html
from util import make_dict

URL = 'https://nl.wikipedia.org/wiki/Robert_en_Bertrand'
XPATH_EXPR = '//*[@id="Albums"]/parent::h2/following-sibling::ul/li'
ALL_FIELDS = ('Nummer', 'Titel', 'Jaar')
FIELDS = ('Nummer', 'Titel')


if __name__ == "__main__":
    r = requests.get(URL)
    doc = html.fromstring(r.text)
    l = doc.xpath(XPATH_EXPR)
    make_d = partial(make_dict, header=ALL_FIELDS, fields=FIELDS)
    # Rows are like this: 1. Mysterie op Rozendael, 1973
    data = list(list(e.strip() for e in elements.text_content().replace('.',',').split(',')) for elements in l)

    print(tabulate(map(make_d, data), headers='keys', tablefmt='tsv'))

