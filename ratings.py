from models import School, Race, Rating, db
from collections import defaultdict


def rating_for(school):
    rating_query = db.session.query(Rating).filter(Rating.school_id == school.id).order_by(Rating.date.desc())
    return rating_query.first().rating


def matchups_for(school_id):
    races = db.session.query(Race).filter((Race.school_id == school_id) | (Race.opponent_id == school_id)).order_by(Race.date.desc()).all()
    school_ids = []
    for race in races:
        school_ids.append(race.school_id)
        school_ids.append(race.opponent_id)
    ratings = db.session.query(Rating).filter(Rating.school_id.in_(list(set(school_ids)))).all()
    rating_data = defaultdict(dict)
    for rating in ratings:
        rating_data[rating.school_id][rating.date] = rating
    data = []
    for i, race in enumerate(races):
        for race in races:
            if race.school_id == school_id:
                opponent_id = race.opponent_id
                opponent_score = race.opponent_score
                school_score = race.school_score
            else:
                opponent_id = race.school_id
                opponent_score = race.school_score
                school_score = race.opponent_score
            data.append({
                'opponent_id': opponent_id,
                'school_score': school_score,
                'opponent_score': opponent_score,
                'date': race.date.strftime("%b %d, %Y"),
                'school_rating': rating_data[school_id][race.date].rating,
                'opponent_rating': rating_data[opponent_id][race.date].rating,
                'school_rd': rating_data[school_id][race.date].rd,
                'opponent_rd': rating_data[opponent_id][race.date].rd
                })
    return data
