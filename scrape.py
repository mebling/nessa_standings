from scraper import Scraper
from datetime import date
from app import app
from models import db, School, Rating, Race
from arena import Arena
from tqdm import tqdm


def scrape_all():
    # TODO get this to be valid
    year = 2018 - 2000
    while Scraper(year).scrape():
        year += 1
    Scraper().scrape()
    _rebuild_ratings()


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


if __name__ == '__main__':
    with app.app_context():
        scrape_all()
