from datetime import date
from tqdm import tqdm
import boto3
import json
from collections import defaultdict, namedtuple

from scraper import Scraper
from arena import Arena


Rating = namedtuple('Rating', 'school_id date rating rd')


def scrape_all():
    year = 0
    schools = {}
    races = defaultdict(list)
    while Scraper(schools, races, year).scrape():
        year += 1
    Scraper(schools, races).scrape()
    schools = list(schools.values())
    all_races = defaultdict(list)
    for s_id, school_races in races.items():
        for r in school_races:
            if not all_races.get(r.opponent_id):
                all_races[s_id].extend(r)
    ratings = _ratings(schools, [item for sublist in all_races.values() for item in sublist])
    _write_index_json_file(schools, ratings)
    _write_school_json_files(schools, races, ratings)


def _ratings(schools, races):
    matchups = [[race.date, race.school_id, race.opponent_id, race.school_score, race.opponent_score] for race in races]
    arena = Arena(matchups)
    dates = arena.dates
    ratings = defaultdict(list)
    for school in tqdm(schools):
        all_ratings = arena.ratings_for(school.id)
        rds = arena.rds_after(school.id)
        for rating, rd, date in zip(all_ratings, rds, dates):
            rating = Rating(school_id=school.id, rating=rating, rd=rd, date=date)
            ratings[school.id].append(rating)
    return ratings


def _write_index_json_file(schools, ratings):
    schools = [{'name': school.name, 'id': school.id, 'rating': ratings[school.id][-1]} for school in schools]
    schools = sorted(schools, key=lambda k: k['rating'], reverse=True)
    _write_json_file({'schools': schools}, 'index')


def _write_school_json_files(schools, races, ratings):
    for school in tqdm(schools):
        _write_json_file({'matchups': _matchups_for(school.id, races[school.id], ratings)}, school.id)


def _matchups_for(school_id, races, ratings):
    school_ids = [school_id]
    for race in races:
        school_ids.append(race.opponent_id)
    ratings = []
    for s_id in school_ids:
        ratings.extend(ratings[s_id])
    rating_data = defaultdict(dict)
    for rating in ratings:
        rating_data[rating.school_id][rating.date] = rating
    data = []
    for i, race in enumerate(races):
        for race in races:
            opponent_id = race.opponent_id
            opponent_score = race.opponent_score
            school_score = race.school_score
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


def _write_json_file(json_data, filename):
    s3 = boto3.resource('s3')
    s3_object = boto3.resource('s3').Object('nessa_rankings', '{}.json'.format(filename))
    s3_object.put(
        Body=(bytes(json.dumps(json_data).encode('UTF-8')))
    )


if __name__ == '__main__':
    scrape_all()
