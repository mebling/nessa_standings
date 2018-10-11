from functools import lru_cache
from base_scraper import BaseScraper
from models import School, Race
from dateutil import parser


BASE_URL = "http://taboracademy.net/nessa/"


class ResultsScraper(BaseScraper):
    def __init__(self, link):
        self.name = link.text_content()
        self.url = BASE_URL + link.attrib['href']

    @property
    @lru_cache()
    def _school(self):
        external_id = int(self.url.split("schoolid=")[1])
        return School.get(external_id=external_id)

    # The keys are Date, Opponent, Result, Score, Comments
    def _create_race(self, match):
        print(match)
        school_score, opponent_score = match['Score'].replace(" ", "").split("-")[0:2]
        date = str(parser.parser(match['Date']))
        opponent_name = match['Opponent'].replace('At ', '')
        opponent_school = School.get(name=opponent_name)
        Race.find_or_create(school_id=self._school.id, opponent_id=opponent_school.id, date=date, school_score=school_score, opponent_score=opponent_score)

    def scrape(self):
        tr_elements = self._doc.xpath('//tr')
        columns = [t.text_content() for t in tr_elements[0]]
        for elem in tr_elements[1:]:
            match = {}
            for col, val in zip(columns, elem):
                match[col] = val.text_content()
            self._create_race(match)
