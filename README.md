# Hackathon Sniper

It is a simple automated tool that scans web for upcoming hackathons and sends notifs via discord Webhooks

## v1.0-mvp

-**Core:** Python engine with BeautifulSoup and DuckDuckGo Search

-**Brain:** Local LLM analysis with Ollama

-**Notifs:** Discord Embeds with already sent link tracking

## Usage

1. Install requirements:
`pip install -r requirements.txt`

2. Set your webhook in `.env`

3. Add search queries to `data/queries.txt`

4. Run:
`python main.py`
