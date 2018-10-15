from glicko import Glicko, WIN, LOSS
from models import School, Race, db
from collections import defaultdict
from tqdm import tqdm
from datetime import datetime, timedelta
from datetime import date as python_date
from copy import copy
from glicko_competitor import GlickoCompetitor
from arena import GlickoArena
import json
import random
from functools import lru_cache


DRAW = None
WIN = True
LOSS = False


def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def matchup(school_a, school_b):
    return True


@lru_cache()
def ratings(date=None):
    data = {}
    dates = db.session.query(Race.date).order_by(Race.date).distinct().all()
    dates = [d.date for d in dates]
    min = dates[0]
    max = datetime.now()
    saved_state = None
    arena = GlickoArena(matchup, base_competitor=GlickoCompetitor)
    arena.add_competitors([school.id for school in db.session.query(School.id).all()])
    for race_date in tqdm(date_range(min, python_date.today())):
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
        arena.tournament(matchups, outcomes)
        data[race_date] = arena.export_state()
    return arena, data


@lru_cache()
def chart_data():
    schools = dict(db.session.query(School.id, School.name).all())
    all_data = defaultdict(list)
    for race_date, data in ratings()[1].items():
        for school_id, values in data.items():
            previous_rating = 1500 if len(all_data[school_id]) == 0 else all_data[school_id][-1][1]
            change = values['initial_rating'] - previous_rating
            change = "+{}".format(str(round(change, 2))) if change >= 0 else str(round(change, 2))
            all_data[school_id].append([race_date.strftime('%m-%d-%Y'), values['initial_rating']])
    chart_data = [{ 'name': schools[school_id], 'data': data } for school_id, data in all_data.items()]
    return chart_data


def rating_for(school):
    arena, _ = ratings()
    return arena.competitors[school.id].rating
