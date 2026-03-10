import time
import requests
from ddgs import DDGS
from bs4 import BeautifulSoup

class Sniper:
    def __init__(self):
        self.ddgs = DDGS()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
        })
    def search_events(self, query, max_results=5):
        print(f'Searching for {query}')
        results = []
        try:
            raw_results = self.ddgs.text(query, max_results=max_results)
            if not raw_results:
                print('    Empty!!!')
                return results
            for res in raw_results:
                results.append({
                    'title': res.get('title'),
                    'link': res.get('href'),
                    'snipper': res.get('body')
                })
        except Exception as e:
            print(f'Got an error: {e}')
        return results
    def scrape_page(self, url):
        try:
            resp = self.session.get(url, timeout=5)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                for el in soup(['script', 'style', 'nav', 'footer']):
                    el.extract()
                text = soup.get_text(separator=' ', strip=True)
                return text[:1000]
            return f"status. {resp.status_code}"
        except Exception as e:
            return f"error. {e}"

if __name__ == '__main__':
    sniper = Sniper()
    queries = [
        "NASA Space Apps Challenge 2026 registration",
        "Ensemble AI hackathon 2026",
        "machine learning quant hackathon travel reimbursement 2026",
        "elite AI hackathon Europe travel covered"
    ]
    for q in queries:
        found = sniper.search_events(q, max_results=3)
        for idx, event in enumerate(found):
            title = event.get('title', 'No title')
            link = event.get('link') or event.get('href', 'No link')
            context = event.get('snippet') or event.get('body', 'No description')
            print(f"\n{idx+1}. {title}")
            print(f"    link. {link}")
            if link != 'No link':
                content = sniper.scrape_page(link)
                print(content[:200])
        time.sleep(2.5)
