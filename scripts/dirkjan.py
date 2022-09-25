#!/usr/bin/env python3
# By Apie 2021-03-04
# License: MIT
import requests
from functools import partial
from tabulate import tabulate

from lxml import html
from util import make_dict

URL = 'https://nl.wikipedia.org/wiki/DirkJan'
XPATH_EXPR = '//*[@id="Hoofdreeks"]/parent::h3/following-sibling::ul[1]/li'
ALL_FIELDS = ('Titel', 'Jaar')
FIELDS = ('Titel', )


if __name__ == "__main__":
    r = requests.get(URL)
    doc = html.fromstring(r.text)
    l = doc.xpath(XPATH_EXPR)
    make_d = partial(make_dict, header=ALL_FIELDS, fields=FIELDS)
    # Rows are like this: DirkJan 1 (1996)
    data = list(list(e.strip() for e in elements.text_content().replace(')','').split('(')) for elements in l)

    print(tabulate(map(make_d, data), headers='keys', tablefmt='tsv'))

