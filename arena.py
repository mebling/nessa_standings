from elote.arenas.lambda_arena import LambdaArena
from collections import defaultdict


class GlickoArena(LambdaArena):
    def add_competitors(self, names):
        for name in names:
            self.competitors[name] = self.base_competitor(**self.base_competitor_kwargs)

    def set_competitor_class_var(self, name, value):
        setattr(self.base_competitor, name, value)

    def tournament(self, matchups, outcomes):
        grouped = defaultdict(list)
        for (a, b), outcome in zip(matchups, outcomes):
            grouped[self.competitors[a]].append([self.competitors[b], outcome])
            grouped[self.competitors[b]].append([self.competitors[a], not outcome])
        for competitor_name, competitor in self.competitors.items():
            competitor.raced(grouped[competitor])
