from glicko import Glicko, WIN, LOSS
from models import School, Race, GlickoRating, db
from collections import defaultdict
from tqdm import tqdm
from datetime import datetime
from copy import copy


def create_ratings():
    scores = defaultdict(Glicko)
    races = db.session.query(Race).filter_by(Race.cached.is_(False)).order_by(Race.date)
    for race in races:
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
        rating = GlickoRating(race_id=race.id, school_id=school.id, rating=scores[school.name].rating.mu)
        db.session.add(rating)
        race.cached = True
        db.session.add(race)
        db.session.commit()
    return scores


# TODO need to list by school
# values I need are race_data, opponent_name, school_name, rating
def chart_data():
    OpponentSchool = db.aliased(School)
    chart_data = []
    tooltip_data = defaultdict(dict)

    glicko_ratings = (db.session
                        .query(GlickoRating.rating, Race.date, OpponentSchool.name, School.name, Race.school_score, Race.opponent_score)
                        .join(Race, Race.id == GlickoRating.race_id)
                        .join(School, School.id == Race.school_id)
                        .join(OpponentSchool, OpponentSchool.id==Race.opponent_id)
                        .order_by(GlickoRating.school_id, Race.date))
    count = glicko_ratings.count()
    data = []
    previous_rating = 1500
    previous_school = None
    for i, (rating, race_date, opponent_name, school_name, school_score, opponent_score) in enumerate(glicko_ratings):
        data.append([datetime.combine(race_date, datetime.min.time()).timestamp(), rating])
        change = rating - previous_rating
        change = "+{}".format(str(round(change, 2))) if change >= 0 else str(round(change, 2))
        tooltip_data[school_name][race_date] = "<b>{}</b><br/>{}<br/>{}-{} ({})".format(race_date.strftime("%b %d, %Y"), opponent_name, school_score, opponent_score, change)
        if i == count-1 or school_name != previous_school:
            chart_data.append({'name': school_name, 'data': data})
            data = []
        previous_rating = rating
        previous_school = school_name
    return chart_data, tooltip_data
