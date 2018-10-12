from glicko import Glicko, WIN, LOSS
from models import School, Race, GlickoRating, db
from collections import defaultdict
from tqdm import tqdm
import datetime
from copy import copy


def create_ratings():
    scores = defaultdict(Glicko)
    race_query = Race.select(Race.id, Race.school_id, Race.opponent_score, Race.school_score, Race.opponent_id).order_by(Race.date)
    for race in tqdm(race_query):
        school = race.school_id
        opponent = race.opponent_id
        opponent_rating = scores[opponent.name]

        # rate the school
        series = [[WIN, opponent_rating.rating]] * race.school_score
        series.extend([[LOSS, opponent_rating.rating]] * race.opponent_score)
        scores[school.name].rate(series)

        # rate the opponent
        opponent_series = [[LOSS, scores[school.name].rating]] * race.school_score
        opponent_series.extend([[WIN, scores[school.name].rating]] * race.opponent_score)
        scores[opponent.name].rate(opponent_series)

        # insert into the database
        GlickoRating.create(race_id=race.id, school_id=school.id, rating=scores[school.name].rating.mu)
        GlickoRating.create(race_id=race.id, school_id=opponent.id, rating=scores[opponent.name].rating.mu)
    return scores


def chart_data():
    chart_data = []
    tooltip_data = defaultdict(dict)
    glicko_ratings = (GlickoRating
                        .select(Race.date, Race.opponent_id, Race.school_score, Race.opponent_score, GlickoRating.race_id, GlickoRating.rating, GlickoRating.school_id, School.name, School.id)
                        .join(Race, on=(Race.id==GlickoRating.race_id))
                        .join(School, on=(School.id==GlickoRating.school_id))
                        .order_by(School.name, Race.date))
    data = []
    for i, rating in tqdm(enumerate(glicko_ratings)):
        race = rating.race_id
        previous_rating = glicko_ratings[i-1].rating if i > 0 else 1500
        data.append([race.date, rating.rating])
        change = rating.rating - previous_rating
        change = "+{}".format(str(round(change, 2))) if change >= 0 else str(round(change, 2))
        tooltip_data[rating.school_id.name][race.date] = "<b>{}</b><br/>{}<br/>{}-{} ({})".format(datetime.datetime.fromtimestamp(race.date/1000.0).strftime("%b %d, %Y"), race.opponent_id.name, race.school_score, race.opponent_score, change)
        if i == len(glicko_ratings)-1 or rating.school_id.name != glicko_ratings[i+1].school_id.name:
            chart_data.append({'name': rating.school_id.name, 'data': data})
            data = []
    return chart_data, tooltip_data


chart_data()
