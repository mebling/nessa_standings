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
            for i in range(race.school_score):
                matchups.append([race.school_id, race.opponent_id])
                outcomes.append(True)
            for i in range(race.opponent_score):
                matchups.append([race.school_id, race.opponent_id])
                outcomes.append(False)
        arena.tournament(race_date, matchups, outcomes)
    return arena


def chart_data():
    schools = dict(db.session.query(School.id, School.name).all())
    chart_data = []
    for school_id in arena().competitors.keys():
        data = [[date.strftime("%b-%d-%Y"), arena().ratings[date][school_id]] for date in sorted(arena().ratings.keys())]
        chart_data.append({ 'name': schools[school_id], 'data': data })
    return chart_data


def rating_for(school):
    return arena().competitors[school.id].rating
