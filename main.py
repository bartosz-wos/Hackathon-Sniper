import time
import os
from pathlib import Path

from src.sniper.scraper import Scraper
from src.sniper.brain import Brain
from src.sniper.discord import DCNotifier

WEBHOOK_URL = ''
DATA_DIR = Path('data')
SEEN_FILE = DATA_DIR / 'seen.txt'

def load_seen():
    if not SEEN_FILE.exists(): return set()
    return set(SEEN_FILE.read_text().splitlines())

def save_seen(url):
    with open(SEEN_FILE, 'a') as f:
        f.write(f'{url}\n')

def main():
    print('engine started\n')

    scraper = Scraper()
    brain = Brain()
    discord = DCNotifier(WEBHOOK_URL)

    seen_links = load_seen()
    queries = [i for i in (DATA_DIR / 'queries.txt').read_text().splitlines() if i.strip()]
    prompt = (DATA_DIR / 'prompt.txt').read_text(encoding='utf-8')

    for q in queries:
        results = scraper.search_events(q, max_results=3)

        for ev in results:
            url = ev.get('href')
            if not url or url in seen_links: continue

            print(f'scanning. {url}')

            content = scraper.get_text(url)
            if content.startswith(('error', 'status')):
                print('download error')
                seen_links.add(url)
                save_seen(url)
                continue

            analysis = brain.analyze(content, url, prompt)

            if analysis.get('is_hackathon'):
                is_future_event = brain.norm_to_bool(analysis.get('is_future_event'))
                print(f'    found new event, sending to dc')
                
                if is_future_event:
                    discord.send(analysis, url)

            seen_links.add(url)
            save_seen(url)
            time.sleep(2)

if __name__ == '__main__':
    main()
