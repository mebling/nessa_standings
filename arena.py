from rating_periods import RatingPeriods
from match import Match


class Arena:
    def __init__(self, matchups):
        self.rating_periods = RatingPeriods([Match(*m) for m in matchups])

    def ratings_for(self, competitor):
        return self.rating_periods.ratings_for(competitor)

    def rating_for(self, competitor):
        return self.ratings_for(competitor)[-1]

    @property
    def dates(self):
        return self.rating_periods.dates

    def rating_on(self, date, competitor):
        return self.rating_periods.rating_on(date, competitor)
