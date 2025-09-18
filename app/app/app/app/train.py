"""Train model and persist artifact."""
import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingClassifier
from pathlib import Path

DATA_DIR = Path("./data/processed")
MODEL_DIR = Path("./data/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def train_and_save():
dfs = list(DATA_DIR.glob("historical_games_*.csv"))
if not dfs:
raise FileNotFoundError("No processed historical data found")
frames = [pd.read_csv(f) for f in dfs]
df = pd.concat(frames, ignore_index=True)

features = ["rating_diff", "rest_diff", "inj_diff"]
df = df.dropna(subset=features + ["home_score", "away_score"])

y = (df["home_score"] > df["away_score"]).astype(int)
X = df[features]

model = GradientBoostingClassifier()
model.fit(X, y)

joblib.dump({"model": model, "features": features}, MODEL_DIR / "latest_model.joblib")
print("Saved model to", MODEL_DIR / "latest_model.joblib")


if __name__ == "__main__":
train_and_save()
