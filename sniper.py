import time
import datetime
import json
import requests
from ddgs import DDGS
from bs4 import BeautifulSoup
import ollama

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

    def analyze(self, text, url):
        today = datetime.date.today().strftime('%Y-%m-%d')

        prompt = f"""
        Dzisiejsza data to: {today}.
        Otrzymujesz tekst zeskrapowany z sieci (URL: {url}).
        
        ZASADY:
        Szukaj informacji o hackathonach. Ignoruj menu i powtórzenia. Jeśli tekst wspomina o hackathonie, uznaj to za sukces.
           
        Zwróć TYLKO czysty obiekt JSON. Nie dodawaj żadnego tekstu przed ani po JSON-ie.
        {{
            "reasoning": "Opisz tu krótko swój tok myślenia. Czy to hackathon? Czy data jest po {today}?",
            "is_hackathon": boolean,
            "name": "Nazwa wydarzenia (lub null)",
            "is_future_event": boolean (lub null),
            "is_paid": "free" / "paid" / "unknown",
            "travel_reimbursement": boolean (lub null),
            "location": "Sama nazwa miasta i kraju (lub null, jeśli nie podano)"
        }}

        Tekst ze strony:
        {text[:2500]}
        """

        try:
            resp = ollama.chat(model='llama3', messages=[
                {'role': 'user', 'content': prompt}
            ], format='json')
            raw_output = resp['message']['content']
            print(raw_output)
            return json.loads(raw_output)
        except Exception as e:
            return {'error': str(e), 'is_hackathon': False}

def normalize_bool(val):
    if isinstance(val, bool): return val
    if isinstance(val, str):
        v = val.lower().strip()
        if v in ['true', 'tak', 'yes', '1', 't']: return True
    return False

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
                if not content.startswith('error') and not content.startswith('status'):
                    print('    ---Analysis---')
                    analysis = sniper.analyze(content, link)
                    if analysis.get('is_hackathon'):
                        is_future = normalize_bool(analysis.get('is_future_event'))
                        print('    Found a crazy ahhh Hackathon!')
                        print(f"        name. {analysis.get('name')}")
                        print(f"        location. {analysis.get('location')}")
                        print(f"        future event. {'TAK' if is_future else 'NIE'}")
                        print(f"        transport refund. {analysis.get('travel_reimbursement')}")
                    else:
                        print('    Not hackathon or wrong data')
                else:
                    print(f"    Skipped, cause of error: {content}")
        time.sleep(2.5)
