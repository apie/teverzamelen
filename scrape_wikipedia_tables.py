#!/usr/bin/env python3
"""
Scrape a table from wikipedia using python. Allows for cells spanning multiple rows and/or columns. Outputs csv files for
each table
url: https://gist.github.com/wassname/5b10774dfcd61cdd3f28
authors: panford, wassname, muzzled, Yossi, apie (convert to class)
license: MIT
"""

from bs4 import BeautifulSoup
import requests
import sys


class Parser:
    def __init__(self, url, table_nr=0, header_start=0):
        self.url = url
        self.table_nr = table_nr
        self.header_start = header_start
        header = {
            'User-Agent': 'Mozilla/5.0'
        }  # Needed to prevent 403 error on Wikipedia
        page = requests.get(self.url, headers=header)
        soup = BeautifulSoup(page.content, "html.parser")

        self.tables = soup.findAll("table", {"class": ["wikitable", "toccolours"]})

        self.tdata = {}
        for tn, table in enumerate(self.tables):
            # preinit list of lists
            rows = table.findAll("tr")
            row_lengths = [len(r.findAll(['th', 'td'])) for r in rows]
            ncols = max(row_lengths)
            nrows = len(rows)
            self.tdata[tn] = []
            for i in range(nrows):
                rowD = []
                for j in range(ncols):
                    rowD.append('')
                self.tdata[tn].append(rowD)

            # process html
            for i in range(len(rows)):
                row = rows[i]
                rowD = []
                cells = row.findAll(["td", "th"])
                for j in range(len(cells)):
                    cell = cells[j]

                    #lots of cells span cols and rows so lets deal with that
                    cspan = int(cell.get('colspan', 1))
                    rspan = int(cell.get('rowspan', 1))
                    l = 0
                    for k in range(rspan):
                        # Shifts to the first empty cell of this row
                        while self.tdata[tn][i + k][j + l]:
                            l += 1
                        for m in range(cspan):
                            cell_n = j + l + m
                            row_n = i + k
                            # in some cases the colspan can overflow the table, in those cases just get the last item
                            cell_n = min(cell_n, len(self.tdata[tn][row_n])-1)
                            self.tdata[tn][row_n][cell_n] += cell.text.strip()

                if rowD:
                    self.tdata[tn].append(rowD)

    def get_header(self):
        return self.tdata[self.table_nr][self.header_start]

    def get_data(self):
        return self.tdata[self.table_nr][self.header_start + 1:]

    def print(self):
        # show tables
        for i, table in enumerate(self.tables):
            print("#"*10 + "Table {}".format(i) + '#'*10)
            print(table.text[:100])
            print('.'*80)
        print("#"*80)


if __name__ == '__main__':
    p = Parser(sys.argv[1])
    p.print()
