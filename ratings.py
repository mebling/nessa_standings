from glicko import Glicko
from models import School, Race, db
from collections import defaultdict
from tqdm import tqdm


def get_rating(team_name, date):
    return glicko_scores(date)[team_name].rating.rated_at


def glicko_scores(date):
    scores = defaultdict(Glicko)
    milliseconds = int(round(date.timestamp() * 1000))
    school_mapping = {}
    race_query = Race.select(Race.school_id, Race.opponent_score, Race.school_score, Race.opponent_id).where(Race.date <= milliseconds).order_by(Race.date)
    for race in tqdm(race_query):
        school = race.school_id
        opponent = race.opponent_id
        opponent_rating = scores[opponent.name]
        series = [[1, opponent_rating.rating]] * race.school_score
        series.extend([[0, opponent_rating.rating]] * race.opponent_score)
        scores[school.name].rate(series)
    return scores


from dateutil import parser
import datetime
date = parser.parse("03/12/2014")
rating = get_rating('Wellesley High School', datetime.datetime.now())
print(rating)
