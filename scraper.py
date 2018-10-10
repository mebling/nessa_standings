import requests
import lxml.html as lh
import pandas as pd


BASE_URL = "http://taboracademy.net/nessa/"
URL = BASE_URL + "standings.asp"
YEARS = ["_09", "_10", "_11", "_12", "_13", "_14", "_15", "_16", "_17", ""]


def scrape(url):
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    links = doc.xpath('//tr//a')[2:]
    for link in links:
        school_name = link.text_content()
        results_link = BASE_URL + link.attrib['href']


def scrape_all():
    for year in YEARS:
        scrape(URL + year)


if __name__ == '__main__':
    scrape_all()
