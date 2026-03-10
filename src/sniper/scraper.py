import requests
from ddgs import DDGS
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.ddgs = DDGS()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
        })

    def search_events(self, query, max_results=3):
        print(f'searching for {query} in ddgs')

        try:
            return self.ddgs.text(query, max_results=max_results) or []
        except Exception as e:
            print(f'error. {e}')
            return []

    def get_text(self, url, max_length=2500):
        try:
            resp = self.session.get(url, timeout=5)
            if resp.status_code != 200:
                return f'status. {resp.status_code}'

            soup = BeautifulSoup(resp.text, 'html.parser')

            for el in soup(['script', 'style', 'nav', 'footer']):
                el.extract()

            return soup.get_text(separator=' ', strip=True)[:max_length]
        except Exception as e:
            return f'error. {e}'

