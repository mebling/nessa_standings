import math


class GlickoRating:
    C = 1
    Q = 0.0057565

    def __init__(self, rating=1500, rd=350):
        self.rating = rating
        self.rd = self._transformed_rd(rd)
        self.matches = {}

    def _transformed_rd(self, rd):
        return min([350, math.sqrt(rd ** 2 + self.C ** 2)])

    @property
    def _g(self):
        return (math.sqrt(1 + 3 * (self.Q ** 2) * self.rd ** 2 / math.pi ** 2))

    def _expected_score(self, glicko_rating):
        exponent = (-1 * glicko_rating._g * (self.rating - glicko_rating.rating)) / 400.
        return 1 / (1 + 10 ** exponent)

    def compete(self, glicko_rating, outcome):
        self.matches[glicko_rating] = 1. if outcome else (.5 if outcome == None else 0.)
        glicko_rating.matches[self] = 0. if outcome else (.5 if outcome == None else 1.)

    @property
    def end_glicko_rating(self):
        if len(self.matches) == 0:
            return GlickoRating(self.rating, self.rd)
        d_square_inv = 0
        difference = 0
        for glicko_rating, actual_score in self.matches.items():
            impact = glicko_rating._g
            expected_score = self._expected_score(glicko_rating)
            difference += impact * (actual_score - expected_score)
            d_square_inv += (expected_score * (1 - expected_score) * (self.Q ** 2) * (impact ** 2))

        denom = self.rd ** -2 + d_square_inv
        rating = self.rating + self.Q / denom * difference
        rd = math.sqrt(1. / denom)
        return GlickoRating(rating, rd)
