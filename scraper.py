import requests
import lxml.html as lh
import pandas as pd
from datetime import datetime


BASE_URL = "http://taboracademy.net/nessa/"
URL = BASE_URL + "standings.asp"
START_YEAR = 9


class Scraper:
    def __init__(self, url, year=None):
        self.year = year
        self.url = url
        if not year:
            self.url = url
        elif year < 10:
            self.url = url.replace("nessa", "nessa_0{}".format(year))
        else:
            self.url = url.replace("nessa", "nessa_{}".format(year))

    @property
    def _doc(self):
        page = requests.get(self.url)
        return lh.fromstring(page.content)

    @property
    def _school_links(self):
        return self._doc.xpath('//tr//a')[2:]

    @property
    def can_scrape(self):
        return "Detailed Error" not in self._doc.text_content()

    def scrape(self):
        print("SCRAPING FOR THE YEAR '{}".format(self.year))
        for link in self._school_links:
            SchoolScraper(link).scrape()


class SchoolScraper:
    def __init__(self, link):
        self.school_name = link.text_content()
        self.school_url = link.attrib['href']

    def scrape(self):
        print("SCRAPING FOR {}".format(self.school_name), "needs to be implemented")
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
