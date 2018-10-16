from collections import defaultdict


class RatingPeriod:
    def __init__(self, arena, date, matchups, outcomes):
        self.arena = arena
        self.matchups = matchups
        self.outcomes = outcomes
        self.date = date
        self.rds = {}
        self.ratings = {}

    def commit(self):
        for competitor_id, competitor in self.arena.competitors.items():
            competitor.update()
            self.rds[competitor_id] = competitor.rd
            self.ratings[competitor_id] = competitor.rating

    def rating_for(self, competitor_id):
        return self.ratings[competitor_id]

    def run(self):
        grouped = defaultdict(list)
        for (a, b), outcome in zip(self.matchups, self.outcomes):
            grouped[self.arena.competitors[a]].append([self.arena.competitors[b], outcome])
            grouped[self.arena.competitors[b]].append([self.arena.competitors[a], not outcome])
        for competitor_name, competitor in self.arena.competitors.items():
            competitor.transform_rd(min_rd=350)
        for competitor_name, competitor in self.arena.competitors.items():
            competitor.raced(grouped[competitor])
        self.commit()
