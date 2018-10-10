from scraper import Scraper


START_YEAR = 10


def scrape_all():
    year = START_YEAR
    while Scraper(year).scrape():
        year += 1
    Scraper().scrape()


if __name__ == '__main__':
    scrape_all()
