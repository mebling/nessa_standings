from glicko_rating import GlickoRating


class RatingPeriod:
    def __init__(self, competitors, matches, previous_rating_period=None):
        self.matches = matches
        self.previous_rating_period = previous_rating_period
        self.glicko_ratings = {}
        self._set_glicko_ratings(competitors)

    def _set_glicko_ratings(self, competitors):
        previous = {}
        for c in competitors:
            if self.previous_rating_period:
                previous[c] = self.previous_rating_period.glicko_rating_for(c)
            else:
                previous[c] = GlickoRating()
        for match in self.matches:
            a_glicko = previous[match.competitor_a]
            previous[match.competitor_a].compete(previous[match.competitor_b], match.outcome)
        for c in competitors:
            self.glicko_ratings[c] = previous[c].end_glicko_rating

    def glicko_rating_for(self, competitor):
        return self.glicko_ratings[competitor]

    def rating_for(self, competitor):
        return self.glicko_rating_for(competitor).rating
