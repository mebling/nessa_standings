import math
from elote.competitors.base import BaseCompetitor


class GlickoCompetitor(BaseCompetitor):
    """ from http://www.glicko.net/glicko/glicko.pdf"""
    _c = 1
    _q = 0.0057565

    def __init__(self, initial_rating=1500, initial_rd=350):
        self.rating = initial_rating
        self.rd = initial_rd

    def __repr__(self):
        return '<GlickoCompetitor: %s>' % (self.__hash__())

    def __str__(self):
        return '<GlickoCompetitor>'

    def export_state(self):
        return {
            "initial_rating": self.rating,
            "initial_rd": self.rd
        }

    @property
    def transformed_rd(self):
        return min([350, math.sqrt(self.rd ** 2 + self._c ** 2)])

    @property
    def _g(self):
        return (math.sqrt(1 + 3 * (self._q ** 2) * self.rd ** 2 / math.pi ** 2))

    def expected_score(self, competitor):
        exponent = (-1 * competitor._g * (self.rating - competitor.rating)) / 400.
        return 1 / (1 + 10 ** exponent)

    def raced(self, races):
        d_square_inv = 0
        difference = 0
        for competitor, outcome in races:
            impact = competitor._g
            expected_score = self.expected_score(competitor)
            actual_score = 1. if outcome else 0.
            difference += impact * (actual_score - expected_score)
            d_square_inv += (
                expected_score * (1 - expected_score) *
                (self._q ** 2) * (impact ** 2))
        denom = self.rd ** -2 + d_square_inv
        rating = self.rating + self._q / denom * difference
        rd = math.sqrt(1. / denom)

        # assign new rating and rd
        self.rating = rating
        self.rd = rd
