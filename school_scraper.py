from base_scraper import BaseScraper
from models import School


URL = "http://www.kistcon.com/nessa/enter.asp"


class SchoolScraper(BaseScraper):
    def __init__(self):
        self.url = URL

    def scrape(self):
        fields = self._doc.xpath("//select[@name='school1']//option")
        for field in fields[1:]:
            school_name = field.text_content().replace("\r\n", "")
            School.find_or_create(school_name)
