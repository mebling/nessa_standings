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
        self.races = defaultdict(list)

    def _add_competitors(self, names):
        for name in names:
            if name not in self.competitors:
                self.competitors[name] = GlickoCompetitor()

    def tournament(self, date, matchups, outcomes):
        grouped = defaultdict(list)
        for (a, b), outcome in zip(matchups, outcomes):
            grouped[self.competitors[a]].append([self.competitors[b], outcome])
            grouped[self.competitors[b]].append([self.competitors[a], not outcome])
            self.races[a].append(date)
            self.races[b].append(date)
        for competitor_name, competitor in self.competitors.items():
            # if team has competed in last 15 months -> we have min_rd=150 else 250
            dates = [d for d in self.races[competitor_name] if d < date]
            min_rd = 350
            if len(dates) > 0:
                d2 = dates[-1]
                months_since_competed = (date.year - d2.year) * 12 + date.month - d2.month
                if months_since_competed > 1:
                    if months_since_competed <= 15:
                        min_rd = 150
                    elif months_since_competed <= 30:
                        min_rd = 250
            competitor.raced(grouped[competitor], min_rd=min_rd)
            self.ratings[date][competitor_name] = competitor.rating
            self.rds[date][competitor_name] = competitor.rd
