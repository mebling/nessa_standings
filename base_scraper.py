from functools import lru_cache
import requests
import lxml.html as lh


class BaseScraper:
    @property
    @lru_cache()
    def _doc(self):
        page = requests.get(self.url)
        return lh.fromstring(page.content)
