"""
Generates 10,000+ synthetic CDR rows for XGBoost scam classifier training.

Feature distributions based on:
  - ITU-T Technical Paper on Telecom Fraud (2023)
  - IEEE: "CDR-based Fraud Detection using ML" (2022)
  - NCRB Cybercrime Report (2024)

Distributions are overlapping (Beta/Poisson/lognormal with shared support) rather
than hard-separated ranges, and ~6% of rows are "hard" cases (label noise +
ambiguous mid-range values) so no single feature perfectly separates the
classes. This keeps the downstream XGBoost model from collapsing onto one
dominant feature and forces it to combine several signals, which is what a
real CDR fraud classifier has to do.

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
HARD_CASE_RATIO = 0.06  # ambiguous rows that blend both distributions
LABEL_NOISE_RATIO = 0.02  # rows where the label is flipped after generation

OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "scam-classifier", "data", "cdr_training_data.csv"
)

AGE_GROUPS = ["18-25", "26-35", "36-45", "46-55", "55-65", "65+"]
AGE_WEIGHTS_SCAM = [0.08, 0.12, 0.15, 0.20, 0.22, 0.23]  # elderly skew, softened
AGE_WEIGHTS_NORMAL = [0.18, 0.22, 0.22, 0.16, 0.13, 0.09]

HOUR_WEIGHTS_SCAM = [1] * 6 + [3, 5, 8, 10, 10, 10, 8, 8, 5, 3, 2, 2, 1, 1, 1, 1, 1, 1]
HOUR_WEIGHTS_NORMAL = [1] * 24  # uniform


def _clip01(x):
    return float(np.clip(x, 0.0, 1.0))


def _beta_score(a, b):
    """Beta-distributed score in [0, 1] — overlapping tails vs. a hard cutoff."""
    return round(_clip01(np.random.beta(a, b)), 2)


def _blend_hour(weights_a, weights_b, mix=0.75):
    """Mostly weights_a, occasionally weights_b — softens the peak-hour signal."""
    weights = weights_a if random.random() < mix else weights_b
    return random.choices(range(24), weights=weights)[0]


def generate_scam_row():
    return {
        # lognormal median ~545s, long right tail overlaps short normal calls
        "call_duration_sec": int(np.clip(np.random.lognormal(6.3, 1.0), 15, 7200)),
        "caller_risk_score": _beta_score(6, 3),  # mean ~0.67, tail reaches down to ~0.2
        "is_international_origin": int(random.random() < 0.55),
        "time_of_day_hour": _blend_hour(HOUR_WEIGHTS_SCAM, HOUR_WEIGHTS_NORMAL, mix=0.8),
        "script_similarity_max": _beta_score(5, 3),  # mean ~0.625
        "urgency_phrase_count": int(np.random.poisson(6)),
        "caller_complaint_count": int(np.random.poisson(8)),
        "callee_age_group": random.choices(AGE_GROUPS, weights=AGE_WEIGHTS_SCAM)[0],
        "call_count_from_number_24h": int(np.clip(np.random.lognormal(4.0, 0.9), 1, 800)),
        "spoofing_indicator": _beta_score(5, 3),
        "is_scam": 1,
    }


def generate_normal_row():
    return {
        # lognormal median ~90s, right tail overlaps long scam calls
        "call_duration_sec": int(np.clip(np.random.lognormal(4.5, 1.1), 5, 5400)),
        "caller_risk_score": _beta_score(2, 6),  # mean ~0.25, tail reaches up to ~0.6
        "is_international_origin": int(random.random() < 0.12),
        "time_of_day_hour": _blend_hour(HOUR_WEIGHTS_NORMAL, HOUR_WEIGHTS_SCAM, mix=0.9),
        "script_similarity_max": _beta_score(2, 5),  # mean ~0.286
        "urgency_phrase_count": int(np.random.poisson(0.8)),
        "caller_complaint_count": int(np.random.poisson(1.2)),
        "callee_age_group": random.choices(AGE_GROUPS, weights=AGE_WEIGHTS_NORMAL)[0],
        "call_count_from_number_24h": int(np.clip(np.random.lognormal(1.6, 0.9), 1, 200)),
        "spoofing_indicator": _beta_score(2, 5),
        "is_scam": 0,
    }


def generate_hard_case_row():
    """Ambiguous row: mixes scam-ish and normal-ish signals for a given label.

    Real fraud calls aren't always textbook — e.g. a short, low-urgency scam
    call, or a long, high-risk-score legitimate telemarketing call. Sampling
    each feature independently from either distribution (instead of always
    the "textbook" one) produces rows that don't fit either template cleanly.
    """
    label = 1 if random.random() < SCAM_RATIO else 0
    scam_row = generate_scam_row()
    normal_row = generate_normal_row()
    row = {}
    for key in scam_row:
        if key == "is_scam":
            continue
        row[key] = scam_row[key] if random.random() < 0.5 else normal_row[key]
    row["is_scam"] = label
    return row


def main():
    hard_count = int(TOTAL_ROWS * HARD_CASE_RATIO)
    remaining = TOTAL_ROWS - hard_count
    scam_count = int(remaining * SCAM_RATIO)
    normal_count = remaining - scam_count

    rows = [generate_scam_row() for _ in range(scam_count)]
    rows += [generate_normal_row() for _ in range(normal_count)]
    rows += [generate_hard_case_row() for _ in range(hard_count)]
    random.shuffle(rows)

    # Label noise: a small fraction of real-world reports are mislabeled
    # (agent misclassification, delayed complaint resolution, etc.).
    noise_count = int(len(rows) * LABEL_NOISE_RATIO)
    for idx in random.sample(range(len(rows)), noise_count):
        rows[idx]["is_scam"] = 1 - rows[idx]["is_scam"]

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    final_scam = sum(r["is_scam"] for r in rows)
    print(
        f"Generated {len(rows)} CDR rows "
        f"({final_scam} scam, {len(rows) - final_scam} normal, "
        f"{hard_count} hard cases, {noise_count} label-noise flips) -> {OUT_PATH}"
    )


if __name__ == "__main__":
    main()
