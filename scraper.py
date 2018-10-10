import requests
import lxml.html as lh
import pandas as pd
from datetime import datetime


BASE_URL = "http://taboracademy.net/nessa/"
URL = BASE_URL + "standings.asp"
START_YEAR = 9


class Scraper:
    def __init__(self, url, year=None):
        self.url = url
        if not year:
            self.url = url
        elif year < 10:
            self.url = url + "_0{}".format(year)
        else:
            self.url = url + "_{}".format(year)

    @property
    def _school_links(self):
        page = requests.get(self.url)
        doc = lh.fromstring(page.content)
        return doc.xpath('//tr//a')[2:]

    def scrape(self):
        for link in self._school_links:
            SchoolScraper(link).scrape()


class SchoolScraper:
    def __init__(self, link):
        self.school_name = link.text_content()
        self.school_url = link.attrib['href']

    def scrape(self):
        pass


def scrape_all():
    year = START_YEAR
    while True:
        scraper = Scraper(URL, year)
        if not scraper.can_scrape:
            Scraper(URL).scrape()
            return
        scraper.scrape()
        year += 1


if __name__ == '__main__':
    scrape_all()
