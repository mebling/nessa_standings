from scraper import Scraper
import datetime
from app import app


START_YEAR = 9


def scrape_all():
    year = START_YEAR
    while Scraper(year).scrape():
        year += 1
    Scraper().scrape()


if __name__ == '__main__':
    with app.app_context():
        scrape_all()
