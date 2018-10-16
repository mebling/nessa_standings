from collections import defaultdict
from glicko_competitor import GlickoCompetitor
from rating_period import RatingPeriod


class GlickoArena():
    def __init__(self, competitors, initial_state=None):
        self.competitors = dict()
        if initial_state is not None:
            for k, v in initial_state.items():
                self.competitors[k] = GlickoCompetitor(**v)
        self._add_competitors(competitors)
        self.rating_periods = {}

    def _add_competitors(self, names):
        for name in names:
            if name not in self.competitors:
                self.competitors[name] = GlickoCompetitor()

    def tournament(self, date, matchups, outcomes):
        rating_period = RatingPeriod(self, date, matchups, outcomes)
        rating_period.run()
        self.rating_periods[date] = rating_period

    @property
    def dates(self):
        return sorted([rating_period.date for rating_period in self.rating_periods.values()])

    def ratings_for(self, competitor_name):
        return [self.rating_periods[date].rating_for(competitor_name) for date in self.dates]

    def rating_on(self, date, competitor_name):
        return self.rating_periods[date].rating_for(competitor_name)
