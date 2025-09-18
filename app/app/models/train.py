"""Train a simple logistic regression for home win probability and save model."""
import os
from pathlib import Path
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, accuracy_score

DATA_DIR = Path(os.environ.get("DATA_DIR", "./data"))
RAW_DIR = DATA_DIR / "raw"
MODEL_DIR = Path(os.environ.get("MODEL_PATH", "./data/models/latest_model.joblib")).parent
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def load_data(csv_path: Path):
    df = pd.read_csv(csv_path, parse_dates=["date"]).sort_values("date")
    return df


def featurize(df: pd.DataFrame):
    df = df.copy()
    df["home_win"] = (df["home_score"] > df["away_score"]).astype(int)
    df["rating_diff"] = df["home_rating"] - df["away_rating"]
    df["rest_diff"] = df["home_rest"] - df["away_rest"]
    df["inj_diff"] = df.get("home_injuries", 0).fillna(0) - df.get("away_injuries", 0).fillna(0)
    features = ["rating_diff", "rest_diff", "inj_diff"]
    X = df[features].fillna(0)
    y = df["home_win"]
    return X, y


if __name__ == "__main__":
    sample_csv = RAW_DIR / "historical_games_sample.csv"
    if not sample_csv.exists():
        raise SystemExit("No sample CSV found. Run etl.py --download-sample first.")
    df = load_data(sample_csv)
    X, y = featurize(df)
    model = LogisticRegression(max_iter=500)
    model.fit(X, y)
    preds = model.predict_proba(X)[:, 1]
    print("Train Brier:", brier_score_loss(y, preds))
    model_path = MODEL_DIR / "latest_model.joblib"
    joblib.dump({"model": model, "features": ["rating_diff", "rest_diff", "inj_diff"]}, model_path)
    print("Saved model to", model_path)
