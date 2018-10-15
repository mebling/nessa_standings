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
        return 1 / (math.sqrt(1 + 3 * cls._q ** 2 * self.rd ** 2 / math.pi ** 2))

    def expected_score(self, competitor):
        exponent = (-1 * competitor._g * (self.rating - competitor.rating)) / 400.
        return 1 / (1 + 10 ** exponent)

    def raced(self, races):
        d2_sum = 0
        r_sum = 0
        for (competitor, outcome) in races:
            s = 1 if outcome else 0
            E_term = self.expected_score(competitor)
            d2_sum += competitor._g ** 2 * E_term * (1 - E_term)
            r_sum += competitor._g) * (s - E_term)
        d_squared = (self._q ** 2 * d2_sum) ** -1
        new_r = (self.rating + (self._q / (1 / self.rd ** 2 + 1 / d_squared))) * r_sum
        new_rd = math.sqrt(((1 / self.rd ** 2) + (1 / d_squared)) ** -1)

        # assign new rating and rd
        self.rating = new_r
        self.rd = new_rd
