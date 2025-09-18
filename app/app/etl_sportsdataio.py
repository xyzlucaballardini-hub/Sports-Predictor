"""ETL helpers for SportsDataIO (v3) - NBA/MLB/NFL box scores, injuries, odds.

This file implements:
- fetch_games_by_date(sport, date)
- fetch_box_scores_by_date(sport, date)
- fetch_injuries(sport)
- ingest_daily(date, out_dir)

Notes:
- SportsDataIO requires header `Ocp-Apim-Subscription-Key: {key}` or query param `key=`.
- Adjust endpoints if your account uses a different version or custom path.
"""
import os
import time
import requests
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()
API_KEY = os.getenv("SPORTSDATAIO_KEY")
BASE = os.getenv("SPORTSDATAIO_BASE", "https://api.sportsdata.io")
DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
RAW_DIR = DATA_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"Ocp-Apim-Subscription-Key": API_KEY}

# session with retries
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=(429, 500, 502, 503, 504))
session.mount("https://", HTTPAdapter(max_retries=retries))


def _get(url, params=None, timeout=20):
    params = params or {}
    resp = session.get(url, headers=HEADERS, params=params, timeout=timeout)
    if resp.status_code == 429:
        # rate-limit: exponential backoff
        wait = int(resp.headers.get("Retry-After", "5"))
        time.sleep(wait)
        resp = session.get(url, headers=HEADERS, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def fetch_games_by_date(sport: str, date_str: str):
    """Return list of games for the sport on the given ISO date (YYYY-MM-DD).

    Example sport strings: 'nba', 'nfl', 'mlb'
    """
    # Example endpoint: /v3/nba/scores/json/GamesByDate/{date}
    url = f"{BASE}/v3/{sport}/scores/json/GamesByDate/{date_str}"
    data = _ge
