from glicko_rating import GlickoRating
import numpy as np


class RatingPeriod:
    def __init__(self, competitors, matches, previous_rating_period=None, adjust_score=False):
        self.adjust_score = adjust_score
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


    def _adjust_all_ratings(self):
        if not self.adjust_score:
            pass
        ratings = []
        for c in self.competitors:
            rating = self.previous_rating_period.glicko_rating_for(c)
            ratings.append(rating.rating)
        mean = np.average(ratings)
        standard_deviation = np.std(rating)
        for c in self.competitors:
            rating = self.previous_rating_period.glicko_rating_for(c)
            rating.adjust(mean, standard_deviation)


    def glicko_rating_for(self, competitor):
        return self.glicko_ratings[competitor]

    def rating_on(self, competitor):
        return self.glicko_rating_for(competitor).rating

    def rating_after(self, competitor):
        return self.glicko_rating_for(competitor).end_glicko_rating.rating

    def rd_on(self, competitor):
        return self.glicko_rating_for(competitor).rd

    def rd_after(self, competitor):
        return self.glicko_rating_for(competitor).end_glicko_rating.rd
