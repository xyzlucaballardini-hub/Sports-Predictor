from flask import Flask, request, jsonify
import joblib
import os
from dotenv import load_dotenv
from app.utils import american_to_prob, prepare_features_for_api

load_dotenv()
app = Flask(__name__)
MODEL_PATH = os.environ.get("MODEL_PATH", "/data/models/latest_model.joblib")

# load model at startup
_meta = joblib.load(MODEL_PATH)
MODEL = _meta["model"]
FEATURES = _meta["features"]


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/predict/game", methods=["POST"])
def predict_game():
    """Expect JSON: {rating_diff, rest_diff, inj_diff, closing_home_odds}
    Returns model_prob, market_prob, edge
    """
    payload = request.json or {}
    X = prepare_features_for_api(payload, FEATURES)
    prob = float(MODEL.predict_proba(X)[0, 1])
    closing = payload.get("closing_home_odds")
    market_prob = None
    edge = None
    if closing is not None:
        market_prob = american_to_prob(float(closing))
        edge = prob - market_prob
    return jsonify({"model_prob": prob, "market_prob": market_prob, "edge": edge})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
