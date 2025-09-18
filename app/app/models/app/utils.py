import math
import pandas as pd


def american_to_prob(odds: float) -> float:
    # Convert American odds to implied probability
    if odds > 0:
        return 100.0 / (odds + 100.0)
    else:
        return -odds / (-odds + 100.0)


def prepare_features_for_api(payload: dict, feature_names):
    # payload should contain rating_diff/rest_diff/inj_diff keys
    row = [payload.get(k, 0) for k in feature_names]
    return pd.DataFrame([row], columns=feature_names)
