from results_scraper import ResultsScraper
from functools import lru_cache
from base_scraper import BaseScraper


URL = "http://taboracademy.net/nessa/standings.asp"


class Scraper(BaseScraper):
    def __init__(self, year=None):
        self.year = year
        if not year:
            self.url = URL
        elif year < 10:
            self.url = URL.replace("nessa", "nessa_0{}".format(year))
        else:
            self.url = URL.replace("nessa", "nessa_{}".format(year))

    @property
    @lru_cache()
    def _school_links(self):
        tr_elements = self._doc.xpath("//tr")
        links = []
        for elem in tr_elements:
            is_link = elem[0][0].attrib.get('href')
            if len(elem) == 7 and is_link:
                links.extend(elem[0])
        return links

    @property
    @lru_cache()
    def is_valid(self):
        return "Detailed Error" not in self._doc.text_content()

    def scrape(self):
        print("SCRAPING FOR THE YEAR '{}".format(self.year))
        if self.is_valid:
            for link in self._school_links:
                ResultsScraper(self.url.split("standings.asp")[0], link).scrape()
            return True
        return False
