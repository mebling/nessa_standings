from functools import lru_cache
from dateutil import parser
import time
from collections import namedtuple

from base_scraper import BaseScraper

BASE_URL = "http://taboracademy.net/nessa/"


School = namedtuple('School', 'id name')
Race = namedtuple('Race', 'school_id opponent_id date school_score opponent_score')

NAME_MAPPINGS = {
  'Bishop Hendricken High School' : 'Bishop Hendricken HS',
  'Bishop Hendricken  HS': 'Bishop Hendricken HS',
  'Boston Latin School':'Boston Latin High School',
  'Portland HS':'Portland High School',
  "St. Sebastian's Country Day School":"St Sebastian's School",
  'Sturgis East Charter School':'Sturgis Charter School',
  'Swampscott High School':'Swampscott HS',
  'Valley Regional High School ':'Valley Regional High School',
  'Valley Regional High School \xa0':'Valley Regional High School'
}


class ResultsScraper(BaseScraper):
    def __init__(self, schools, races, url, link):
        self.schools = schools
        self.races = races
        self.name = link.text_content()
        self.url = url + link.attrib['href']

    def _school(self, name=None):
        name = NAME_MAPPINGS.get(name or self.name, name or self.name)
        school = self.schools.get(name, School(name=name, id=name))
        self.schools[school.id] = school
        return school

    def _create_race(self, match):
        print(match)
        results = [int(s) for s in match['Score'].replace(" ", "").split("-") if s != ""]
        school_score, opponent_score = results
        date = parser.parse(match['Date'])
        opponent_name = match['Opponent'].replace('At ', '')
        opponent_school = self._school(opponent_name)
        school_score, opponent_score = sorted(results, reverse=match['Result'] == 'Win')
        race = Race(school_id=self._school().id, opponent_id=opponent_school.id, date=date.date(), school_score=school_score, opponent_score=opponent_score)
        self.races[self._school().id].append(race)

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
        return True
