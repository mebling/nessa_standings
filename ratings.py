from glicko import Glicko, WIN, LOSS
from models import School, Race, GlickoRating, db
from collections import defaultdict
from tqdm import tqdm
import datetime
from copy import copy


def create_ratings():
    scores = defaultdict(Glicko)
    race_query = Race.select(Race.id, Race.school, Race.opponent_score, Race.school_score, Race.opponent).order_by(Race.date)
    for race in tqdm(race_query):
        school = race.school
        opponent = race.opponent
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
        GlickoRating.create(race=race.id, school=school.id, rating=scores[school.name].rating.mu)
        GlickoRating.create(race=race.id, school=opponent.id, rating=scores[opponent.name].rating.mu)
    return scores


# TODO need to list by school
def chart_data():
    OpponentSchool = School.alias()
    chart_data = []
    tooltip_data = defaultdict(dict)
    glicko_ratings = (GlickoRating
                        .select(Race, OpponentSchool, GlickoRating, School)
                        .join(Race, on=(Race.id==GlickoRating.race))
                        .join(School, on=(School.id==GlickoRating.school))
                        .join(OpponentSchool, on=(Race.opponent==OpponentSchool.id))
                        .order_by(School.name, Race.date))
    data = []
    for i, rating in enumerate(glicko_ratings):
        previous_rating = glicko_ratings[i-1].rating if i > 0 else 1500
        data.append([rating.race.date, rating.rating])
        change = rating.rating - previous_rating
        change = "+{}".format(str(round(change, 2))) if change >= 0 else str(round(change, 2))
        tooltip_data[rating.school.name][rating.race.date] = "<b>{}</b><br/>{}<br/>{}-{} ({})".format(datetime.datetime.fromtimestamp(rating.race.date/1000.0).strftime("%b %d, %Y"), rating.race.opponent.name, rating.race.school_score, rating.race.opponent_score, change)
        if i == len(glicko_ratings)-1 or rating.school.name != glicko_ratings[i+1].school.name:
            chart_data.append({'name': rating.school.name, 'data': data})
            data = []
    return chart_data, tooltip_data


print(chart_data())
