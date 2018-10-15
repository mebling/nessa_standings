from functools import lru_cache
from base_scraper import BaseScraper
from models import School, Race, db
from dateutil import parser
import time

BASE_URL = "http://taboracademy.net/nessa/"


class ResultsScraper(BaseScraper):
    def __init__(self, season, url, link):
        self.season = season
        self.name = link.text_content()
        self.url = url + link.attrib['href']

    @property
    @lru_cache()
    def _school(self):
        return School.find_or_create(name=self.name)

    def _create_race(self, match):
        print(match)
        results = [s for s in match['Score'].replace(" ", "").split("-") if s != ""]
        school_score, opponent_score = results
        date = parser.parse(match['Date'])
        opponent_name = match['Opponent'].replace('At ', '')
        opponent_school = School.find_or_create(name=opponent_name)
        status = match['Result']
        score_a, score_b = results
        if status == "Win":
            school_score = max(score_a, score_b)
            opponent_score = min(score_a, score_b)
        else:
            opponent_score = max(score_a, score_b)
            school_score = min(score_a, score_b)
        Race.find_or_create(season_id=self.season.id, school_id=self._school.id, opponent_id=opponent_school.id, date=date, school_score=school_score, opponent_score=opponent_score)

    def scrape(self):
        while True:
            try:
                tr_elements = self._doc.xpath('//tr')
                break
            except:
                time.sleep(1)

        columns = [t.text_content() for t in tr_elements[0]]
        for elem in tr_elements[1:]:
            match = {}
            for col, val in zip(columns, elem):
                match[col] = val.text_content()
            self._create_race(match)
