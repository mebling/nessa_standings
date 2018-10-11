from scraper import Scraper
from school_scraper import SchoolScraper
from ratings import glicko_scores
import datetime


START_YEAR = 9


def scrape_all():
    SchoolScraper().scrape()
    year = START_YEAR
    while Scraper(year).scrape():
        year += 1
    Scraper().scrape()


if __name__ == '__main__':
    scrape_all()
    scores = glicko_scores(datetime.datetime.now())
    for school_name, rating in scores.items():
        print("{}: {}".format(school_name, rating.rating.mu))
