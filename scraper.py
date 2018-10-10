import requests
import lxml.html as lh
import pandas as pd


BASE_URL = "http://taboracademy.net/nessa/"
URL = BASE_URL + "standings.asp"
YEARS = ["_09", "_10", "_11", "_12", "_13", "_14", "_15", "_16", "_17", ""]


class Scraper:
    def __init__(self, url):
        self.url = url

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
    for year in YEARS:
        Scraper(URL + year).scrape()


if __name__ == '__main__':
    scrape_all()
