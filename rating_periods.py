from datetime import date, timedelta
from rating_period import RatingPeriod


class RatingPeriods:
    def __init__(self, matches):
        self.rating_periods = {}
        self.matches = matches
        self._add_rating_periods()

    def _add_rating_periods(self):
        min_date = min([m.date for m in self.matches])
        previous = None
        for d in self.dates:
            period_matches = [m for m in self.matches if m.date == d]
            rating_period = RatingPeriod(self._competitors, period_matches, previous_rating_period=self.rating_periods.get(previous))
            self.rating_periods[d] = rating_period
            previous = d

    @property
    def _competitors(self):
        comps = []
        for match in self.matches:
            comps.extend([match.competitor_a, match.competitor_b])
        return list(set(comps))

    @property
    def dates(self):
        min_date = min([m.date for m in self.matches])
        return [min_date + timedelta(n) for n in range(int((date.today() - min_date).days))]

    def ratings_for(self, competitor):
        return [self.rating_periods[date].rating_for(competitor) for date in self.dates]

    def rating_on(self, date, competitor):
        return self.rating_periods[date].rating_for(competitor)
