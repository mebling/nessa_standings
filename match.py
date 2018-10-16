class Match:
    def __init__(self, date, competitor_a, competitor_b, a_score, b_score):
        self.date = date
        self.competitor_a = competitor_a
        self.competitor_b = competitor_b
        self.a_score = a_score
        self.b_score = b_score

    @property
    def outcome(self):
        if self.a_score > self.b_score:
            return True
        elif self.b_score > self.a_score:
            return False
        else:
            return None
