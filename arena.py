from elote.arenas.lambda_arena import LambdaArena
from collections import defaultdict


class GlickoArena(LambdaArena):
    def set_competitor_class_var(self, name, value):
        setattr(self.base_competitor, name, value)

    def tournament(self, matchups, outcomes):
        grouped = defaultdict(list)
        for (a, b), outcome in zip(matchups, outcomes):
            if a not in self.competitors:
                self.competitors[a] = self.base_competitor(**self.base_competitor_kwargs)
            if b not in self.competitors:
                self.competitors[b] = self.base_competitor(**self.base_competitor_kwargs)
            grouped[self.competitors[a]].append([self.competitors[b], outcome])
            grouped[self.competitors[b]].append([self.competitors[a], not outcome])
        for (competitor, races) in grouped.items():
            competitor.raced(races)
