"""
Generates 10,000+ synthetic CDR rows for XGBoost scam classifier training.

Feature distributions based on:
  - ITU-T Technical Paper on Telecom Fraud (2023)
  - IEEE: "CDR-based Fraud Detection using ML" (2022)
  - NCRB Cybercrime Report (2024)

Run:
    cd ml/data_generation
    python generate_cdr.py

Output: ml/scam-classifier/data/cdr_training_data.csv
"""
import csv
import os
import random

import numpy as np

random.seed(42)
np.random.seed(42)

TOTAL_ROWS = 10000
SCAM_RATIO = 0.30  # 30% scam, 70% normal (class imbalance handled in training)

OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "scam-classifier", "data", "cdr_training_data.csv"
)

AGE_GROUPS = ["18-25", "26-35", "36-45", "46-55", "55-65", "65+"]
AGE_WEIGHTS_SCAM = [0.05, 0.10, 0.15, 0.20, 0.25, 0.25]  # Elderly targeted
AGE_WEIGHTS_NORMAL = [0.20, 0.25, 0.25, 0.15, 0.10, 0.05]

HOUR_WEIGHTS_SCAM = [1] * 6 + [3, 5, 8, 10, 10, 10, 8, 8, 5, 3, 2, 2, 1, 1, 1, 1, 1, 1]
HOUR_WEIGHTS_NORMAL = [1] * 24  # Uniform


def generate_scam_row():
    return {
        "call_duration_sec": int(np.random.lognormal(6.5, 0.8)),  # median ~660s
        "caller_risk_score": round(random.uniform(0.6, 1.0), 2),
        "is_international_origin": int(random.random() < 0.70),
        "time_of_day_hour": random.choices(range(24), weights=HOUR_WEIGHTS_SCAM)[0],
        "script_similarity_max": round(random.uniform(0.70, 0.99), 2),
        "urgency_phrase_count": random.randint(5, 25),
        "caller_complaint_count": random.randint(3, 50),
        "callee_age_group": random.choices(AGE_GROUPS, weights=AGE_WEIGHTS_SCAM)[0],
        "call_count_from_number_24h": random.randint(20, 500),
        "spoofing_indicator": round(random.uniform(0.6, 1.0), 2),
        "is_scam": 1,
    }


def generate_normal_row():
    return {
        "call_duration_sec": int(np.random.lognormal(4.5, 1.0)),  # median ~90s
        "caller_risk_score": round(random.uniform(0.0, 0.3), 2),
        "is_international_origin": int(random.random() < 0.05),
        "time_of_day_hour": random.choices(range(24), weights=HOUR_WEIGHTS_NORMAL)[0],
        "script_similarity_max": round(random.uniform(0.0, 0.30), 2),
        "urgency_phrase_count": random.randint(0, 2),
        "caller_complaint_count": random.randint(0, 1),
        "callee_age_group": random.choices(AGE_GROUPS, weights=AGE_WEIGHTS_NORMAL)[0],
        "call_count_from_number_24h": random.randint(1, 10),
        "spoofing_indicator": round(random.uniform(0.0, 0.2), 2),
        "is_scam": 0,
    }


def main():
    scam_count = int(TOTAL_ROWS * SCAM_RATIO)
    normal_count = TOTAL_ROWS - scam_count

    rows = [generate_scam_row() for _ in range(scam_count)]
    rows += [generate_normal_row() for _ in range(normal_count)]
    random.shuffle(rows)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} CDR rows ({scam_count} scam, {normal_count} normal) -> {OUT_PATH}")


if __name__ == "__main__":
    main()
