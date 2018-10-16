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
        self.rating_periods = []

    def _add_competitors(self, names):
        for name in names:
            if name not in self.competitors:
                self.competitors[name] = GlickoCompetitor()

    def tournament(self, date, matchups, outcomes):
        rating_period = RatingPeriod(date)
        self.rating_periods.append(rating_period)
        grouped = defaultdict(list)
        for (a, b), outcome in zip(matchups, outcomes):
            grouped[self.competitors[a]].append([self.competitors[b], outcome])
            grouped[self.competitors[b]].append([self.competitors[a], not outcome])
        for competitor_name, competitor in self.competitors.items():
            competitor.raced(grouped[competitor], min_rd=350)
            rating_period.add(competitor)
        rating_period.commit()

    @property
    def dates(self):
        return [rating_period.date for rating_period in self.rating_periods]

    def ratings_for(self, competitor_name):
        return [rating_period.rating_for(self.competitors[competitor_name]) for rating_period in self.rating_periods]

    def rating_on(self, date, competitor_name):
        rating_period = [rating_period for rating_period in self.rating_periods if rating_period.date == date][0]
        return rating_period.rating_for(self.competitors[competitor_name])
