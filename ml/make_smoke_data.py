"""Creates tiny synthetic datasets in the exact raw layouts the Primer
manifest builders expect, so train.py can be smoke-tested end-to-end on CPU.
"""
import os
import numpy as np
from PIL import Image
import soundfile as sf

REPO = "/home/user/Primer"

# ── Currency images: data/raw/currency/currency dataset 1.1/data/data/{real,fake}/<denom>/ ──
img_root = os.path.join(REPO, "data", "raw", "currency", "currency dataset 1.1", "data", "data")
rng = np.random.default_rng(42)
for split in ("real", "fake"):
    for denom in ("500", "2000"):
        d = os.path.join(img_root, split, denom)
        os.makedirs(d, exist_ok=True)
        for i in range(10):
            base = 180 if split == "real" else 80
            arr = (rng.normal(base, 40, (128, 256, 3))).clip(0, 255).astype(np.uint8)
            Image.fromarray(arr).save(os.path.join(d, f"note_{i:03d}.jpg"))
print("currency images done")

# ── ASVspoof 2019 LA: protocols + flac dirs ──
la = os.path.join(REPO, "data", "raw", "voice_spoofing", "ASVspoof 2019", "LA")
proto_dir = os.path.join(la, "ASVspoof2019_LA_cm_protocols")
os.makedirs(proto_dir, exist_ok=True)

SPLITS = {
    "train": ("ASVspoof2019.LA.cm.train.trn.txt", "ASVspoof2019_LA_train"),
    "dev": ("ASVspoof2019.LA.cm.dev.trl.txt", "ASVspoof2019_LA_dev"),
    "eval": ("ASVspoof2019.LA.cm.eval.trl.txt", "ASVspoof2019_LA_eval"),
}
sr = 16000
for split, (proto_file, audio_dir) in SPLITS.items():
    flac_dir = os.path.join(la, audio_dir, "flac")
    os.makedirs(flac_dir, exist_ok=True)
    lines = []
    for i in range(16):
        label = "bonafide" if i % 2 == 0 else "spoof"
        file_id = f"LA_{split[0].upper()}_{i:07d}"
        # bonafide: plain tone; spoof: tone + noise, varying lengths 1-5s
        dur = 1.0 + (i % 5)
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        freq = 220 + 40 * i
        y = 0.3 * np.sin(2 * np.pi * freq * t)
        if label == "spoof":
            y = y + rng.normal(0, 0.1, y.shape)
        sf.write(os.path.join(flac_dir, f"{file_id}.flac"), y.astype(np.float32), sr)
        attack = "-" if label == "bonafide" else f"A{(i % 6) + 1:02d}"
        lines.append(f"LA_{i:04d} {file_id} - {attack} {label}")
    with open(os.path.join(proto_dir, proto_file), "w") as f:
        f.write("\n".join(lines) + "\n")
print("asvspoof audio done")
