#!/usr/bin/env python3
# By Apie 2022-09-21
# License: MIT
import re
import requests
from functools import partial
from tabulate import tabulate

from lxml import html
from util import make_dict

URL = 'https://en.m.wikipedia.org/wiki/Nicholas_Sparks'
XPATH_EXPR = '//span[@id="Novels"]/parent::h3/following-sibling::div/ul/li//i'
ALL_FIELDS = ('Titel', 'Jaar')
FIELDS = ('Titel',)


if __name__ == "__main__":
    r = requests.get(URL)
    doc = html.fromstring(r.text)
    l = doc.xpath(XPATH_EXPR)
    # Rows are like this:
    # The Guardian (April 2003) ISBN 978-1-58621-393-0
    # But sometimes nested.
    data = []
    seen = set()
    for element in l:
        # Only keep the title
        title = element.text_content().split('(')[0].strip()
        if title in seen:
            continue
        seen.add(title)
        data.append([title])

    make_d = partial(make_dict, header=ALL_FIELDS, fields=FIELDS)
    print(tabulate(map(make_d, data), headers='keys', tablefmt='tsv'))

