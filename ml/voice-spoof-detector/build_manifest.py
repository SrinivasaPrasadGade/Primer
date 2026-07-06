"""
Parses the ASVspoof 2019 LA protocol files and builds train/dev/eval manifests.

Input:  data/raw/voice_spoofing/ASVspoof 2019/LA/
         ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.{train.trn,dev.trl,eval.trl}.txt
         ASVspoof2019_LA_{train,dev,eval}/flac/<file_id>.flac
Output: ml/voice-spoof-detector/data/{train,dev,eval}_manifest.csv
         columns: filepath, speaker_id, attack_id, label (1=spoof/synthetic, 0=bonafide/genuine)

Protocol line format (whitespace-separated):
    <speaker_id> <file_id> - <attack_id or -> <bonafide|spoof>

Run:
    cd ml/voice-spoof-detector
    python build_manifest.py
"""
import csv
import os

BASE_DIR = os.path.dirname(__file__)
DATASET_DIR = os.path.join(BASE_DIR, "..", "..", "data", "raw", "voice_spoofing", "ASVspoof 2019", "LA")
PROTOCOLS_DIR = os.path.join(DATASET_DIR, "ASVspoof2019_LA_cm_protocols")
OUT_DIR = os.path.join(BASE_DIR, "data")

SPLITS = {
    "train": ("ASVspoof2019.LA.cm.train.trn.txt", "ASVspoof2019_LA_train"),
    "dev": ("ASVspoof2019.LA.cm.dev.trl.txt", "ASVspoof2019_LA_dev"),
    "eval": ("ASVspoof2019.LA.cm.eval.trl.txt", "ASVspoof2019_LA_eval"),
}
LABEL_MAP = {"bonafide": 0, "spoof": 1}


def parse_protocol(protocol_path: str, audio_dir: str) -> list:
    rows = []
    with open(protocol_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) != 5:
                continue
            speaker_id, file_id, _, attack_id, label_name = parts
            filepath = os.path.abspath(os.path.join(audio_dir, "flac", f"{file_id}.flac"))
            if not os.path.isfile(filepath):
                raise FileNotFoundError(f"Missing audio file referenced by protocol: {filepath}")
            rows.append({
                "filepath": filepath,
                "speaker_id": speaker_id,
                "attack_id": attack_id,
                "label": LABEL_MAP[label_name],
            })
    return rows


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for split_name, (protocol_file, audio_subdir) in SPLITS.items():
        protocol_path = os.path.join(PROTOCOLS_DIR, protocol_file)
        audio_dir = os.path.join(DATASET_DIR, audio_subdir)
        rows = parse_protocol(protocol_path, audio_dir)

        out_path = os.path.join(OUT_DIR, f"{split_name}_manifest.csv")
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["filepath", "speaker_id", "attack_id", "label"])
            writer.writeheader()
            writer.writerows(rows)

        n_spoof = sum(1 for r in rows if r["label"] == 1)
        n_bonafide = len(rows) - n_spoof
        print(f"{split_name}: wrote {len(rows)} rows to {out_path} "
              f"({n_bonafide} bonafide, {n_spoof} spoof)")


if __name__ == "__main__":
    main()
