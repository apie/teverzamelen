#!/usr/bin/env python3
# Scrape stripinfo reeks page
# By Apie 2021-10-17
# License: MIT

from bs4 import BeautifulSoup  # type: ignore
import requests
import sys

BASE_URL = 'https://stripinfo.be/reeks/index/'
FIELDS = ('countcol', 'firstcol')


class Parser:
    def __init__(self, url: str, header_start=0):
        self.url = url
        self.session = requests.session()
        self.tdata = []
        page = self.session.get(self.url, timeout=5)
        soup = BeautifulSoup(page.content, "html.parser")
        self.title = soup.findAll("title")[0].text.split(' - stripinfo.be')[0]

        tables = soup.findAll("table", {"class": ["lijst"]})
        assert len(tables) == 1
        table = tables[0]
        rows = table.findAll("tr")
        for row in rows:
            cells = row.findAll("td")
            data = dict()
            for cell in cells:
                for field in FIELDS:
                    if cell.attrs['class'][0] == field:
                        data[field] = cell.text.strip()
            if data:
                self.tdata.append(data)

    def get_data(self):
        return self.tdata


if __name__ == "__main__":
    from tabulate import tabulate
    url = sys.argv[1]
    assert url.startswith(BASE_URL)
    p = Parser(url)
    print(tabulate(p.get_data(), headers='keys', tablefmt='tsv'))

