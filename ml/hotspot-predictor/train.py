"""
Trains the Random Forest Hotspot Predictor on spatiotemporal crime grid data.

Input:  ml/hotspot-predictor/data/hotspot_training_data.csv
         (generate with ml/data_generation/generate_hotspot_data.py;
         optionally enrich first with ml/data_generation/fetch_geo_features.py
         and a real NCRB CSV in data/raw/geo_crime/ — see that script's docstring)
Output: ml/hotspot-predictor/hotspot_predictor.joblib
         (copied to backend/app/ml/models/hotspot_predictor.joblib)

Run:
    cd ml/hotspot-predictor
    python train.py
"""
import json
import os
import shutil

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "hotspot_training_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "hotspot_predictor.joblib")
IMPORTANCE_PATH = os.path.join(BASE_DIR, "feature_importance.json")
BACKEND_MODELS_DIR = os.path.join(BASE_DIR, "..", "..", "backend", "app", "ml", "models")

FEATURES = [
    "latitude", "longitude",
    "crime_count_7d", "crime_count_30d",
    "population_density",
    "bank_atm_density",
    "day_of_week", "month",
    "avg_loss_amount_area",
]
LABEL = "is_hotspot"


def load_data():
    df = pd.read_csv(DATA_PATH)
    return df[FEATURES], df[LABEL]


def main():
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        class_weight="balanced",
        random_state=RANDOM_STATE,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print(classification_report(y_test, y_pred, target_names=["normal", "hotspot"]))
    print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")

    importance = dict(zip(FEATURES, model.feature_importances_.tolist()))
    importance = dict(sorted(importance.items(), key=lambda kv: kv[1], reverse=True))
    print("\nFeature importance:")
    for name, score in importance.items():
        print(f"  {name}: {score:.4f}")

    joblib.dump(model, MODEL_PATH)
    with open(IMPORTANCE_PATH, "w") as f:
        json.dump(importance, f, indent=2)

    os.makedirs(BACKEND_MODELS_DIR, exist_ok=True)
    shutil.copy(MODEL_PATH, os.path.join(BACKEND_MODELS_DIR, "hotspot_predictor.joblib"))

    print(f"\nSaved model -> {MODEL_PATH}")
    print(f"Copied model -> {BACKEND_MODELS_DIR}")


if __name__ == "__main__":
    main()
