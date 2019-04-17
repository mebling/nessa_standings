from datetime import date
from tqdm import tqdm
import boto3
import json

from scraper import Scraper
from app import app
from models import db, School, Rating, Race
from arena import Arena
from ratings import rating_for, matchups_for


def scrape_all():
    year = 9
    while Scraper(year).scrape():
        year += 1
    Scraper().scrape()
    _rebuild_ratings()
    _write_index_json_file()
    _write_school_json_files()


def _rebuild_ratings():
    db.session.flush()
    db.session.query(Rating).delete()
    races = db.session.query(Race).all()
    matchups = [[race.date, race.school_id, race.opponent_id, race.school_score, race.opponent_score] for race in races]
    arena = Arena(matchups)
    schools = db.session.query(School).all()
    dates = arena.dates
    for school in tqdm(schools):
        ratings = arena.ratings_for(school.id)
        rds = arena.rds_after(school.id)
        for rating, rd, date in zip(ratings, rds, dates):
            rating = Rating(school_id=school.id, rating=rating, rd=rd, date=date)
            db.session.add(rating)
        db.session.commit()


def _write_index_json_file():
    schools = db.session.query(School).order_by(School.name).all()
    schools = [{'name': school.name, 'id': school.id, 'rating': rating_for(school)} for school in schools]
    schools = sorted(schools, key=lambda k: k['rating'], reverse=True)
    _write_json_file({'schools': schools}, 'index')


def _write_school_json_files():
    schools = db.session.query(School).all()
    for school in tqdm(schools):
        _write_json_file({'matchups': matchups_for(school.id)}, school.id)


def _write_json_file(json_data, filename):
    s3 = boto3.resource('s3')
    s3_object = boto3.resource('s3').Object('nessa_rankings', '{}.json'.format(filename))
    s3_object.put(
        Body=(bytes(json.dumps(json_data).encode('UTF-8')))
    )


if __name__ == '__main__':
    with app.app_context():
        scrape_all()
