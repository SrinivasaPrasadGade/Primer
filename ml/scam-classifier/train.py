"""
Trains the XGBoost Scam Classifier on synthetic CDR feature data.

Input:  ml/scam-classifier/data/cdr_training_data.csv
         (generate with ml/data_generation/generate_cdr.py)
Output: ml/scam-classifier/scam_classifier.joblib
         (copied to backend/app/ml/models/scam_classifier.joblib)

Run:
    cd ml/scam-classifier
    python train.py
"""
import json
import os
import shutil

import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

RANDOM_STATE = 42

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "cdr_training_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "scam_classifier.joblib")
ENCODER_PATH = os.path.join(BASE_DIR, "callee_age_group_encoder.joblib")
IMPORTANCE_PATH = os.path.join(BASE_DIR, "feature_importance.json")
BACKEND_MODELS_DIR = os.path.join(BASE_DIR, "..", "..", "backend", "app", "ml", "models")

FEATURES = [
    "call_duration_sec",
    "caller_risk_score",
    "is_international_origin",
    "time_of_day_hour",
    "script_similarity_max",
    "urgency_phrase_count",
    "caller_complaint_count",
    "callee_age_group",
    "call_count_from_number_24h",
    "spoofing_indicator",
]
LABEL = "is_scam"


def load_data():
    df = pd.read_csv(DATA_PATH)

    # XGBoost needs numeric input; encode the one categorical feature.
    age_encoder = LabelEncoder()
    df["callee_age_group"] = age_encoder.fit_transform(df["callee_age_group"])

    X = df[FEATURES]
    y = df[LABEL]
    return X, y, age_encoder


def main():
    X, y, age_encoder = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    # Class imbalance (30% scam / 70% normal) handled via scale_pos_weight.
    scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

    model = xgb.XGBClassifier(
        max_depth=6,
        n_estimators=200,
        learning_rate=0.1,
        eval_metric="logloss",
        scale_pos_weight=scale_pos_weight,
        random_state=RANDOM_STATE,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print(classification_report(y_test, y_pred, target_names=["normal", "scam"]))
    print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")

    # Feature importance for the Explainable AI panel.
    importance = dict(zip(FEATURES, model.feature_importances_.tolist()))
    importance = dict(sorted(importance.items(), key=lambda kv: kv[1], reverse=True))
    print("\nFeature importance:")
    for name, score in importance.items():
        print(f"  {name}: {score:.4f}")

    joblib.dump(model, MODEL_PATH)
    joblib.dump(age_encoder, ENCODER_PATH)
    with open(IMPORTANCE_PATH, "w") as f:
        json.dump(importance, f, indent=2)

    os.makedirs(BACKEND_MODELS_DIR, exist_ok=True)
    shutil.copy(MODEL_PATH, os.path.join(BACKEND_MODELS_DIR, "scam_classifier.joblib"))
    shutil.copy(ENCODER_PATH, os.path.join(BACKEND_MODELS_DIR, "callee_age_group_encoder.joblib"))

    print(f"\nSaved model -> {MODEL_PATH}")
    print(f"Copied model -> {BACKEND_MODELS_DIR}")


if __name__ == "__main__":
    main()
