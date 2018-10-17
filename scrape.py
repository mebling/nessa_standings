from scraper import Scraper
from datetime import date
from app import app


def scrape_all():
    year = date.today().year - 2000
    while Scraper(year).scrape():
        year += 1
    Scraper().scrape()


if __name__ == '__main__':
    with app.app_context():
        scrape_all()
