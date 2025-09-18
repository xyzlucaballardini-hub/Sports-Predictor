"""Simple ETL: placeholders for fetching box scores and injuries and saving CSVs.
Usage: python app/etl.py --download-sample
"""
import os
import argparse
from pathlib import Path
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = Path(os.environ.get("DATA_DIR", "./data"))
RAW_DIR = DATA_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def download_sample_csv(out_path: Path):
    # Create a tiny sample dataset for prototyping
    data = [
        {"date":"2024-10-01","home_team":"A","away_team":"B","home_score":100,"away_score":95,"home_rating":5.0,"away_rating":4.0,"home_rest":2,"away_rest":1,"home_injuries":0,"away_injuries":1,"closing_home_odds":-110},
        {"date":"2024-10-02","home_team":"C","away_team":"A","home_score":88,"away_score":92,"home_rating":3.5,"away_rating":5.2,"home_rest":3,"away_rest":2,"home_injuries":2,"away_injuries":0,"closing_home_odds":130},
    ]
    df = pd.DataFrame(data)
    df.to_csv(out_path, index=False)
    print(f"Wrote sample CSV to {out_path}")


def fetch_box_scores_from_api(date_str: str) -> pd.DataFrame:
    """Placeholder: implement calls to your chosen sports API
    Use environment variable SPORTS_API_KEY to authenticate.
    """
    api_key = os.getenv("SPORTS_API_KEY")
    if not api_key:
        raise RuntimeError("SPORTS_API_KEY missing in env")
    # Example: requests.get(...)
    raise NotImplementedError("Replace fetch_box_scores_from_api with real API calls")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--download-sample", action="store_true")
    args = parser.parse_args()
    if args.download_sample:
        download_sample_csv(RAW_DIR / "historical_games_sample.csv")
