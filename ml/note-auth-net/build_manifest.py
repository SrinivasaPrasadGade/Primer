"""
Scans the raw currency image dataset and builds a manifest CSV for training.

Input:  data/raw/currency/currency dataset 1.1/data/data/{real,fake}/<denomination>/*.jpg
Output: ml/note-auth-net/data/manifest.csv
        columns: filepath, denomination, label (1=genuine, 0=counterfeit)

The raw dataset only distinguishes genuine vs. counterfeit per note image — it has
no per-feature (watermark/thread/microprint/intaglio/colour_shift) annotations. Since
NoteAuthNet trains one head per feature, train.py falls back to weak supervision:
every head is trained against the same genuine/counterfeit label. This is a known
simplification, not a modeling choice we'd want in production (see train.py docstring).

Run:
    cd ml/note-auth-net
    python build_manifest.py
"""
import csv
import os

BASE_DIR = os.path.dirname(__file__)
RAW_DIR = os.path.join(BASE_DIR, "..", "..", "data", "raw", "currency", "currency dataset 1.1", "data", "data")
OUT_PATH = os.path.join(BASE_DIR, "data", "manifest.csv")

VALID_EXT = (".jpg", ".jpeg", ".png")
LABEL_DIRS = {"real": 1, "fake": 0}


def scan() -> list:
    rows = []
    for split_name, label in LABEL_DIRS.items():
        split_dir = os.path.join(RAW_DIR, split_name)
        if not os.path.isdir(split_dir):
            raise FileNotFoundError(f"Expected raw data at {split_dir}")
        for denomination in sorted(os.listdir(split_dir)):
            denom_dir = os.path.join(split_dir, denomination)
            if not os.path.isdir(denom_dir):
                continue
            for fname in sorted(os.listdir(denom_dir)):
                if not fname.lower().endswith(VALID_EXT):
                    continue
                rows.append({
                    "filepath": os.path.abspath(os.path.join(denom_dir, fname)),
                    "denomination": denomination,
                    "label": label,
                })
    return rows


def main():
    rows = scan()
    if not rows:
        raise RuntimeError(f"No images found under {RAW_DIR}")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filepath", "denomination", "label"])
        writer.writeheader()
        writer.writerows(rows)

    n_real = sum(1 for r in rows if r["label"] == 1)
    n_fake = len(rows) - n_real
    print(f"Wrote {len(rows)} rows to {OUT_PATH} ({n_real} genuine, {n_fake} counterfeit)")


if __name__ == "__main__":
    main()
