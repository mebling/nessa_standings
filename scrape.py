from scraper import Scraper
from school_scraper import SchoolScraper


START_YEAR = 10


def scrape_all():
    SchoolScraper().scrape()
    year = START_YEAR
    while Scraper(year).scrape():
        year += 1
    Scraper().scrape()


if __name__ == '__main__':
    scrape_all()
