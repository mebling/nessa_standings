from glicko import Glicko, WIN, LOSS
from models import School, Race, db
from collections import defaultdict
from tqdm import tqdm
from datetime import datetime
from copy import copy
from glicko_competitor import GlickoCompetitor
from arena import GlickoArena
import json
import random
from functools import lru_cache


DRAW = None
WIN = True
LOSS = False


def matchup(school_a, school_b):
    return True


def ratings(date=None):
    data = {}
    dates = db.session.query(Race.date).order_by(Race.date).distinct().all()
    saved_state = None
    for date in tqdm(dates):
        races = db.session.query(Race).filter_by(date=date)
        matchups = []
        outcomes = []
        for race in races:
            for i in range(race.school_score):
                matchups.append([race.school_id, race.opponent_id])
                outcomes.append(True)
            for i in range(race.opponent_score):
                matchups.append([race.school_id, race.opponent_id])
                outcomes.append(False)
        arena = GlickoArena(matchup, base_competitor=GlickoCompetitor, initial_state=saved_state)
        arena.tournament(matchups, outcomes)
        data[date.date] = arena.export_state()
    return data


def chart_data():
    tooltip_data = defaultdict(list)
    schools = dict(db.session.query(School.id, School.name).all())
    all_data = defaultdict(list)
    for date, data in ratings().items():
        for school_id, values in data.items():
            previous_rating = 1500 if len(all_data[school_id]) == 0 else all_data[school_id][-1][1]
            change = values['initial_rating'] - previous_rating
            change = "+{}".format(str(round(change, 2))) if change >= 0 else str(round(change, 2))
            tooltip_data[schools[school_id]].append("<b>{}</b><br/>{}".format(date.strftime("%b %d, %Y"), change))
            all_data[school_id].append([date.strftime('%b %d, %Y'), values['initial_rating']])
    chart_data = [{ 'name': schools[school_id], 'data': data } for school_id, data in all_data.items()]
    return chart_data, tooltip_data
