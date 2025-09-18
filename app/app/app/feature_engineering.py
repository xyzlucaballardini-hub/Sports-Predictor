"""Feature engineering utilities.
Takes raw games, boxscores, and injuries and computes features used by models."""
import pandas as pd
import numpy as np
from pathlib import Path

RAW_DIR = Path("./data/raw")
PROC_DIR = Path("./data/processed")
PROC_DIR.mkdir(parents=True, exist_ok=True)


def compute_features(date: str):
# Example: combine injuries and games into features
dfs = []
for sport in ("nba", "nfl", "mlb"):
games_path = RAW_DIR / f"games_{sport}_{date}.csv"
inj_path = RAW_DIR / f"injuries_{sport}_{date}.csv"
if not games_path.exists():
continue
games = pd.read_csv(games_path)
inj = pd.read_csv(inj_path) if inj_path.exists() else pd.DataFrame()

# Simple injury differential: difference in active injuries
inj_counts = inj.groupby("Team").size().reset_index(name="inj_count")
games = games.merge(inj_counts.rename(columns={"Team": "home_team", "inj_count": "home_inj"}),
on="home_team", how="left")
games = games.merge(inj_counts.rename(columns={"Team": "away_team", "inj_count": "away_inj"}),
on="away_team", how="left")
games[["home_inj", "away_inj"]] = games[["home_inj", "away_inj"]].fillna(0)

# Features
games["inj_diff"] = games["home_inj"] - games["away_inj"]
games["rest_diff"] = np.random.randint(-2, 3, len(games)) # placeholder
games["rating_diff"] = np.random.normal(0, 5, len(games)) # placeholder

dfs.append(games)

if dfs:
out = pd.concat(dfs, ignore_index=True)
out.to_csv(PROC_DIR / f"historical_games_{date}.csv", index=False)
print("Wrote", PROC_DIR / f"historical_games_{date}.csv")
return out
else:
print("No data found for date", date)
return None


if __name__ == "__main__":
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--date", required=True)
args = parser.parse_args()
compute_features(args.date)
