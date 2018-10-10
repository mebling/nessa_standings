from functools import lru_cache
from base_scraper import BaseScraper


BASE_URL = "http://taboracademy.net/nessa/"


class SchoolScraper(BaseScraper):
    def __init__(self, link):
        print(link.text_content())
        self.name = link.text_content()
        self.url = BASE_URL + link.attrib['href']

    def scrape(self):
        data = []
        tr_elements = self._doc.xpath('//tr')
        columns = [t.text_content() for t in tr_elements[0]]
        for elem in tr_elements[1:]:
            match = {}
            for col, val in zip(columns, elem):
                match[col] = val.text_content()
            data.append(match)
        print(data)
