#!/usr/bin/env python3
# By Apie 2023-09-09
# License: MIT
# Read a csv downloaded from rebrickable.com containing all the lego sets, filter it on theme and print the result in table format
import csv
from sys import argv
from tabulate import tabulate

theme_id_filter = argv[1] if len(argv) > 1 else 246 # Harry Potter

def get_data():
    with open('sets.csv') as f:
        d = csv.DictReader(f)
        for l in d:
            if l['theme_id'] != str(theme_id_filter):
                continue
            l['set_num'] = l['set_num'].rstrip('-1')
            if not l['set_num'].isnumeric():
                continue
#            print(f"{l['set_num']}: {l['name']}")
            yield {'set_num': l['set_num'], 'name': l['name']}

print(tabulate(get_data(), headers='keys', tablefmt='tsv'))

