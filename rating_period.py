class RatingPeriod:
    def __init__(self, date):
        self.date = date
        self.competitors = []
        self.rds = {}
        self.ratings = {}

    def add(self, competitor):
        self.competitors.append(competitor)

    def commit(self):
        for competitor in self.competitors:
            competitor.update()
            self.rds[competitor] = competitor.rd
            self.ratings[competitor] = competitor.rating

    def rating_for(self, competitor):
        return self.ratings[competitor]
