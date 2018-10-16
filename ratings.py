from models import School, Race, db
from collections import defaultdict
from arena import Arena
from functools import lru_cache


@lru_cache()
def arena(date=None):
    races = db.session.query(Race).all()
    matchups = [[race.date, race.school_id, race.opponent_id, race.school_score, race.opponent_score] for race in races]
    return Arena(matchups)


def chart_data(school_id):
    school = db.session.query(School).filter_by(id=school_id).first()
    data = [[date.strftime("%b-%d-%Y"), rating] for date, rating in zip(arena().dates, arena().ratings_for(school_id))]
    return [{ 'name': school.name, 'data': data }]


def rating_for(school):
    return arena().rating_for(school.id)


def matchups_for(school_id):
    races = db.session.query(Race).filter((Race.school_id == school_id) | (Race.opponent_id == school_id)).order_by(Race.date.desc()).all()
    matchups = defaultdict(list)
    for race in races:
        matchups[race.date].append(race)
    data = []
    dates = arena().dates
    dates.reverse()
    ratings = arena().ratings_for(school_id)
    ratings.reverse()
    rds = arena().rds_on(school_id)
    rds.reverse()
    for i, (date, rating, rd) in enumerate(zip(dates, ratings, rds)):
        races = matchups[date]
        if len(races) == 0:
            continue
        previous_rating = ratings[i + 1] if i + 1 < len(dates) else 1500
        descriptions = []
        for race in races:
            if race.school_id == school_id:
                descriptions.append("{} ({} | {}): {}-{}".format(race.opponent.name, round(arena().rating_on(date, race.opponent_id), 2), round(arena().rd_on(date, race.opponent_id), 2), race.school_score, race.opponent_score))
            else:
                descriptions.append("{} ({} | {}): {}-{}".format(race.school.name, round(arena().rating_on(date, race.school_id), 2), round(arena().rd_on(date, race.school_id) ,2), race.opponent_score, race.school_score))
        description = ", ".join(descriptions)
        data.append({'date': date.strftime("%b %d, %Y"), 'previous_rating': previous_rating, 'rating': rating, 'description': description, 'rd': rd })
    return data
