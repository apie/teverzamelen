#!/usr/bin/env python3
# Scrape lastdodo area page
# By Apie 2024-10-13
# License: MIT

from requests_html import HTMLSession
import sys

BASE_URL = "https://www.lastdodo.nl/nl/areas/"


class Parser:
    def __init__(self, url: str, header_start=0):
        self.url = url
        self.session = HTMLSession()
        self.tdata = []
        page = self.session.get(self.url, timeout=5)
        self.title = page.html.find("title", first=True).text

        items = page.html.find("div.items_container div.card-body")
        for item in items:
            data = {}
            data["year"] = item.find("div.meta > ul > li", first=True).text.strip()
            data["title"] = item.find("div.title", first=True).text.strip()
            self.tdata.append(data)

    def get_data(self):
        return self.tdata


if __name__ == "__main__":
    from tabulate import tabulate

    url = sys.argv[1].strip().strip("#")
    assert url.startswith(BASE_URL)
    p = Parser(url)
    print(tabulate(p.get_data(), headers="keys", tablefmt="tsv"))
