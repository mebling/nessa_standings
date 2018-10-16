from glicko_rating import GlickoRating


class RatingPeriod:
    def __init__(self, competitors, matches, previous_rating_period=None):
        self.matches = matches
        self.previous_rating_period = previous_rating_period
        self.glicko_ratings = {}
        self._set_glicko_ratings(competitors)

    def _set_glicko_ratings(self, competitors):
        for c in competitors:
            if self.previous_rating_period:
                self.glicko_ratings[c] = self.previous_rating_period.glicko_rating_for(c).end_glicko_rating
            else:
                self.glicko_ratings[c] = GlickoRating()
        for match in self.matches:
            self.glicko_ratings[match.competitor_a].compete(self.glicko_ratings[match.competitor_b], match.outcome)

    def glicko_rating_for(self, competitor):
        return self.glicko_ratings[competitor]

    def rating_for(self, competitor):
        return self.glicko_rating_for(competitor).end_glicko_rating.rating

    def rd_for(self, competitor):
        return self.glicko_rating_for(competitor).rd
