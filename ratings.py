from glicko import Glicko, WIN, LOSS
from models import School, Race, db
from collections import defaultdict
from tqdm import tqdm
from datetime import datetime, timedelta
from datetime import date as python_date
from copy import copy
from arena import GlickoArena
import json
import random
from functools import lru_cache


def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


@lru_cache()
def arena(date=None):
    data = {}
    dates = [d.date for d in db.session.query(Race.date).order_by(Race.date).distinct().all()]
    arena = GlickoArena([school.id for school in db.session.query(School.id).all()])
    for race_date in tqdm(date_range(dates[0], python_date.today())):
        if race_date in dates:
            races = db.session.query(Race).filter_by(date=race_date)
        else:
            races = []
        matchups = []
        outcomes = []
        for race in races:
            matchups.append([race.school_id, race.opponent_id])
            if race.school_score > race.opponent_score:
                outcome = True
            elif race.opponent_score < race.school_score:
                outcome = False
            else:
                outcome = None
            outcomes.append(outcome)
        arena.tournament(race_date, matchups, outcomes)
    return arena


def chart_data():
    schools = db.session.query(School).all()
    chart_data = []
    for school in schools:
        print(arena().dates)
        data = [[date.strftime("%b-%d-%Y"), rating] for date, rating in zip(arena().dates, arena().ratings_for(school.id))]
        chart_data.append({ 'name': school.name, 'data': data })
    return chart_data


def rating_for(school):
    return arena().competitors[school.id].rating


def rating_on(school_id, date):
    return arena().rating_on(date, school_id)


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
    for i, (date, rating) in enumerate(zip(dates, ratings)):
        races = matchups[date]
        if len(races) == 0:
            continue
        previous_rating = ratings[i + 1] if i < len(dates) else 1500
        descriptions = []
        for race in races:
            if race.school_id == school_id:
                descriptions.append("{} ({}): {}-{}".format(race.opponent.name, round(rating_on(race.opponent_id, date), 2), race.school_score, race.opponent_score))
            else:
                descriptions.append("{} ({}): {}-{}".format(race.school.name, round(rating_on(race.school_id, date) ,2), race.opponent_score, race.school_score))
        description = ", ".join(descriptions)
        data.append({'date': date.strftime("%b %d, %Y"), 'previous_rating': previous_rating, 'rating': rating, 'description': description})
    return data
