from collections import defaultdict
from glicko_competitor import GlickoCompetitor


class GlickoArena():
    def __init__(self, competitors, initial_state=None):
        self.competitors = dict()
        if initial_state is not None:
            for k, v in initial_state.items():
                self.competitors[k] = GlickoCompetitor(**v)
        self._add_competitors(competitors)
        self.ratings = defaultdict(dict)
        self.rds = defaultdict(dict)

    def _add_competitors(self, names):
        for name in names:
            if name not in self.competitors:
                self.competitors[name] = GlickoCompetitor()

    def tournament(self, date, matchups, outcomes):
        grouped = defaultdict(list)
        for (a, b), outcome in zip(matchups, outcomes):
            grouped[self.competitors[a]].append([self.competitors[b], outcome])
        for competitor_name, competitor in self.competitors.items():
            competitor.raced(grouped[competitor])
            self.ratings[date][competitor_name] = competitor.rating
            self.rds[date][competitor_name] = competitor.rd
