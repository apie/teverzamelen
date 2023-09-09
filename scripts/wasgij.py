#!/usr/bin/env python3
# Scrape WASGIJ product page
# By Apie 2020-10-02
# License: MIT

from typing import Tuple, Iterator

from bs4 import BeautifulSoup, element  # type: ignore
import requests
from requests_cache import NEVER_EXPIRE, CachedSession

from tabulate import tabulate

URL = 'https://wasgij.com/puzzles/'


class Parser:
    def __init__(self, url: str):
        self.url = url
        urls_expire_after = {
            URL+'?sf_paged=*': 600,
            '*': NEVER_EXPIRE,
        }
        self.session = CachedSession('wasgij_cache', urls_expire_after=urls_expire_after)
        self.page = 0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0',
        }

    def _get_number(self, url: str) -> str:
        page = self.session.get(url, headers=self.headers)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
        return soup.find("div", {"class": "number"}).text.strip()

    def _parse_articles(self) -> Iterator[Tuple[str, int, str]]:
        page = self.session.get(f"{self.url}?sf_paged={self.page}", headers=self.headers)
        page.raise_for_status()
        #print(page.url, page.from_cache)
        soup = BeautifulSoup(page.content, "html.parser")
        articles = soup.findAll("article", {"class": "archive-product"})
        assert articles, "No articles found. Stop."
        for article in articles:  # type: element.Tag
            a = article.find("a")
            if 'Retro ' in a.get('title'):
                continue  # Skip retro
            #print(a.get('title'))
            collection_str = article.find("div", {"class": "collection-name"}).text.strip()
            yield collection_str, int(self._get_number(a.get('href'))), a.get('title')

    def get_titles(self):
        while True:
            try:
                yield from self._parse_articles()
            except AssertionError:
                break
            self.page += 1


def sort_wasgij(item: Tuple[str, int, str]) -> str:
    collection, number, title = item
    return f"{collection} {number:>2}"


if __name__ == '__main__':
    p = Parser(URL)
    print(tabulate(
        sorted(set(p.get_titles()), key=sort_wasgij),  # type: ignore
        headers=('Collection', 'Number', 'Title'),
        tablefmt='tsv',
    ))
