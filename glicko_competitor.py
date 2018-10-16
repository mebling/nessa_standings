import math
from elote.competitors.base import BaseCompetitor


class GlickoCompetitor(BaseCompetitor):
    """ from http://www.glicko.net/glicko/glicko.pdf"""
    _c = 1
    _q = 0.0057565

    def __init__(self, initial_rating=1500, initial_rd=350):
        self.rating = initial_rating
        self.rd = initial_rd
        self.rating_period_rating = initial_rating
        self.rating_period_rd = initial_rd

    def export_state(self):
        return {
            "initial_rating": self.rating,
            "initial_rd": self.rd
        }

    def transform_rd(self, min_rd):
        self.rating_period_rd = min([min_rd, math.sqrt(self.rd ** 2 + self._c ** 2)])

    @property
    def _g(self):
        return (math.sqrt(1 + 3 * (self._q ** 2) * self.rd ** 2 / math.pi ** 2))

    def expected_score(self, competitor):
        exponent = (-1 * competitor._g * (self.rating - competitor.rating)) / 400.
        return 1 / (1 + 10 ** exponent)

    def raced(self, races, min_rd=350):
        self.transform_rd(min_rd)
        if len(races) == 0:
            return
        d2_sum = 0
        difference = 0
        for competitor, outcome in races:
            impact = competitor._g
            expected_score = self.expected_score(competitor)
            if outcome:
                actual_score = 1.
            elif outcome == None:
                actual_score = .5
            else:
                actual_score = 0
            difference += impact * (actual_score - expected_score)
            d2_sum += expected_score * (1 - expected_score) * (impact ** 2)
        if d2_sum == 0:
            return
        else:
            d2 = 1/((self._q ** 2) * d2_sum)
            denom = self.rd ** -2 + 1/d2

            # assign new rating and rd
            self.rating_period_rating = self.rating + ((self._q / denom) * difference)
            self.rating_period_pd = math.sqrt(1/denom)

    def update(self):
        self.rating = self.rating_period_rating
        self.rating_period_rd = self.rating_period_rd
