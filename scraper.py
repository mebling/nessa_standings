from results_scraper import ResultsScraper
from functools import lru_cache
from base_scraper import BaseScraper
from models import Season, Race, db
from datetime import date


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
            season = Season.find_or_create(2000 + self.year if self.year else date.today().year)
            races = db.session.query(Race).filter_by(season_id=season.id)
            races.delete()
            db.session.commit()
            for link in self._school_links:
                ResultsScraper(season, self.url.split("standings.asp")[0], link).scrape()
            return True
        return False
