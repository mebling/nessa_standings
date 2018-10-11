from glicko import Glicko, WIN, LOSS
from models import School, Race, db
from collections import defaultdict
from tqdm import tqdm
from functools import lru_cache

def get_rating(team_name, date):
    return glicko_scores(date)[team_name].rating.mu


@lru_cache()
def glicko_scores(date):
    scores = defaultdict(Glicko)
    milliseconds = int(round(date.timestamp() * 1000))
    race_query = Race.select(Race.school_id, Race.opponent_score, Race.school_score, Race.opponent_id).where(Race.date <= milliseconds).order_by(Race.date)
    for race in tqdm(race_query):
        school = race.school_id
        opponent = race.opponent_id
        opponent_rating = scores[opponent.name]
        series = [[WIN, opponent_rating.rating]] * race.school_score
        series.extend([[LOSS, opponent_rating.rating]] * race.opponent_score)
        scores[school.name].rate(series)
    return scores
