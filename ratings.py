from models import School, Race, Rating, db
from collections import defaultdict


def chart_data(school_id):
    ratings = db.session.query(Rating).filter(Rating.school_id == school_id).order_by(Rating.date)
    data = [[rating.date.strftime("%b-%d-%Y"), rating.rating] for rating in ratings]
    rds = [[rating.date.strftime("%b-%d-%Y"), rating.rd] for rating in ratings]
    return [{ 'name': 'Rating', 'data': data }, { 'name': 'RD', 'data': rds }]


def rating_for(school):
    rating_query = db.session.query(Rating).filter(Rating.school_id == school.id).order_by(Rating.date.desc())
    return rating_query.first().rating


def matchups_for(school_id):
    races = db.session.query(Race).filter((Race.school_id == school_id) | (Race.opponent_id == school_id)).order_by(Race.date.desc()).all()
    matchups = defaultdict(list)
    for race in races:
        matchups[race.date].append(race)
    data = []
    school_ids = []
    for race in races:
        school_ids.append(race.school_id)
        school_ids.append(race.opponent_id)
    ratings = db.session.query(Rating).filter(Rating.school_id.in_(list(set(school_ids)))).all()
    rating_data = defaultdict(dict)
    for rating in ratings:
        rating_data[rating.school_id][rating.date] = rating
    ratings = rating_data[school_id]
    dates = list(rating_data[school_id].keys())
    dates.reverse()

    for i, date in enumerate(dates):
        races = matchups[date]
        if len(races) == 0:
            continue
        previous_rating = ratings[dates[i+1]].rating if i + 1 < len(ratings) else 1500
        rating = ratings[date]
        descriptions = []
        for race in races:
            if race.school_id == school_id:
                descriptions.append("{} ({} | {}): {}-{}".format(race.opponent.name, round(rating_data[race.opponent_id][date].rating, 2), round(rating_data[race.opponent_id][date].rd, 2), race.school_score, race.opponent_score))
            else:
                descriptions.append("{} ({} | {}): {}-{}".format(race.school.name, round(rating_data[race.school_id][date].rating, 2), round(rating_data[race.school_id][date].rd ,2), race.opponent_score, race.school_score))
        description = ", ".join(descriptions)
        data.append({'date': date.strftime("%b %d, %Y"), 'previous_rating': previous_rating, 'rating': rating.rating, 'description': description, 'rd': ratings[dates[i+1]].rd })
    return data
