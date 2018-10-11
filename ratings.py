from glicko import Glicko, WIN, LOSS
from models import School, Race, db
from collections import defaultdict
from tqdm import tqdm
from functools import lru_cache
import datetime
from copy import copy


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


def chart_data():
    chart_data = defaultdict(list)
    tooltip_data = defaultdict(dict)

    scores = defaultdict(Glicko)
    race_query = Race.select(Race.school_id, Race.opponent_score, Race.school_score, Race.opponent_id, Race.date).order_by(Race.date)
    for race in tqdm(race_query):
        school = race.school_id
        opponent = race.opponent_id
        opponent_rating = scores[opponent.name]
        series = [[WIN, opponent_rating.rating]] * race.school_score
        series.extend([[LOSS, opponent_rating.rating]] * race.opponent_score)
        previous_rating = copy(scores[school.name])
        scores[school.name].rate(series)
        new_rating = scores[school.name].rating.mu
        chart_data[school.name].append([race.date, scores[school.name].rating.mu])
        change = scores[school.name].rating.mu - previous_rating.rating.mu
        change = "+{}".format(str(round(change, 2))) if change >= 0 else str(round(change, 2))
        tooltip_data[school.name][race.date] = "{}\n -> {}-{} ({})".format(opponent.name, race.school_score, race.opponent_score, change)
    formatted = []
    for key, values in chart_data.items():
        formatted.append({ 'name': key, 'data': values })
    return formatted, tooltip_data
