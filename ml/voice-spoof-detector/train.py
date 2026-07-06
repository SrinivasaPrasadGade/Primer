"""
Trains VoiceSpoofDetector (LCNN on mel-spectrograms) on ASVspoof 2019 LA.

Input:  ml/voice-spoof-detector/data/{train,dev,eval}_manifest.csv
         (generate with ml/voice-spoof-detector/build_manifest.py)
Output: ml/voice-spoof-detector/voice_spoof.pth
         (copied to backend/app/ml/models/voice_spoof.pth)

Uses ASVspoof's own train/dev/eval split (no re-splitting needed - the protocol
files already separate speakers cleanly). "dev" is used for validation/model
selection during training; "eval" is held out and only scored once at the end
as the reported test metric, matching how ASVspoof challenges evaluate models.

Class balance: bonafide (genuine) clips are ~10x rarer than spoof (synthetic)
clips in this dataset, so the loss is weighted inversely by class frequency.

Audio -> model input: each clip is cropped/tiled to exactly 4 seconds (a random
crop for train, a center crop for dev/eval), then converted to a 128-bin mel
spectrogram (n_fft=400 [25ms @ 16kHz], hop_length=160 [10ms]) and z-normalized.
This yields the 128x400 input the LCNN expects.

Reported metric: Equal Error Rate (EER), the standard ASVspoof metric, in
addition to ROC-AUC.

Performance (tuned for RTX 4060, 8GB VRAM):
  - Mixed precision (AMP) is on by default on CUDA. Disable with --no-amp.
  - The classifier outputs logits and the loss is weighted
    binary_cross_entropy_with_logits (AMP-safe). forward() still applies
    sigmoid, so inference callers see probabilities as before, and checkpoints
    remain key-compatible with the previous Sigmoid-in-Sequential layout.
  - --cache-mels precomputes each clip's full-length mel spectrogram to .npy
    (float16) on first touch, then later epochs crop from the cache instead of
    re-decoding FLAC + recomputing mels. Roughly 2-3x faster end-to-end for a
    30-epoch run; costs ~10 GB of disk for train+dev. Cropping the cached mel
    along the time axis is a close approximation of computing the mel on a
    cropped waveform (boundary frames differ; the db offset from ref=max is
    removed by z-normalization).
  - Early stopping (--patience) ends the run when dev EER stops improving.

Run:
    cd ml/voice-spoof-detector
    python train.py --epochs 30 --batch-size 32 --cache-mels
"""
import argparse
import json
import os
import random
import shutil

import librosa
import numpy as np
import pandas as pd
import soundfile as sf
import torch
from sklearn.metrics import roc_auc_score, roc_curve
from torch import nn
from torch.utils.data import DataLoader, Dataset

RANDOM_STATE = 42
SAMPLE_RATE = 16000
CLIP_SECONDS = 4
CLIP_SAMPLES = SAMPLE_RATE * CLIP_SECONDS
N_MELS = 128
N_FFT = 400          # 25ms window at 16kHz
HOP_LENGTH = 160     # 10ms hop at 16kHz
N_FRAMES = CLIP_SAMPLES // HOP_LENGTH  # 400

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
CACHE_DIR = os.path.join(DATA_DIR, "mel_cache")
MODEL_PATH = os.path.join(BASE_DIR, "voice_spoof.pth")
METRICS_PATH = os.path.join(BASE_DIR, "metrics.json")
BACKEND_MODELS_DIR = os.path.join(BASE_DIR, "..", "..", "backend", "app", "ml", "models")


class MFM(nn.Module):
    """Max-Feature-Map activation: splits channels in half and takes the
    element-wise max, halving channel count (Wu et al., LCNN for anti-spoofing).
    """
    def __init__(self, out_channels: int):
        super().__init__()
        self.out_channels = out_channels

    def forward(self, x):
        a, b = torch.split(x, self.out_channels, dim=1)
        return torch.max(a, b)


class VoiceSpoofDetector(nn.Module):
    """Detects AI-generated/synthetic speech.
    Input: mel-spectrogram (128 x 400) from 4-second audio clip
    Output: probability of synthetic speech (0.0 = genuine, 1.0 = synthetic)
    """
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 64, 5, 1, 2), nn.MaxPool2d(2),
            nn.Conv2d(64, 64, 1, 1, 0), MFM(32),
            nn.Conv2d(32, 96, 3, 1, 1), nn.MaxPool2d(2),
            nn.Conv2d(96, 96, 1, 1, 0), MFM(48),
            nn.Conv2d(48, 128, 3, 1, 1), nn.MaxPool2d(2),
            nn.Conv2d(128, 128, 1, 1, 0), MFM(64),
        )
        self.classifier = nn.Sequential(
            nn.Linear(64 * 16 * 50, 256), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(256, 1)
        )

    def forward_logits(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)

    def forward(self, x):
        return torch.sigmoid(self.forward_logits(x))


def fix_length(y: np.ndarray, target_len: int, train: bool, rng: random.Random) -> np.ndarray:
    if len(y) >= target_len:
        start = rng.randint(0, len(y) - target_len) if train else (len(y) - target_len) // 2
        return y[start:start + target_len]
    reps = target_len // len(y) + 1
    return np.tile(y, reps)[:target_len]


def to_mel_db(y: np.ndarray) -> np.ndarray:
    mel = librosa.feature.melspectrogram(y=y, sr=SAMPLE_RATE, n_fft=N_FFT,
                                          hop_length=HOP_LENGTH, n_mels=N_MELS)
    return librosa.power_to_db(mel, ref=np.max)


def fix_frames(mel_db: np.ndarray, train: bool, rng: random.Random) -> np.ndarray:
    if mel_db.shape[1] > N_FRAMES:
        start = rng.randint(0, mel_db.shape[1] - N_FRAMES) if train else (mel_db.shape[1] - N_FRAMES) // 2
        mel_db = mel_db[:, start:start + N_FRAMES]
    elif mel_db.shape[1] < N_FRAMES:
        mel_db = np.pad(mel_db, ((0, 0), (0, N_FRAMES - mel_db.shape[1])), mode="edge")
    return mel_db


def z_normalize(mel_db: np.ndarray) -> np.ndarray:
    return (mel_db - mel_db.mean()) / (mel_db.std() + 1e-6)


class ASVspoofDataset(Dataset):
    def __init__(self, df: pd.DataFrame, train: bool, cache_mels: bool = False):
        self.filepaths = df["filepath"].tolist()
        self.labels = df["label"].astype("float32").to_numpy()
        self.train = train
        self.cache_mels = cache_mels
        self.rng = random.Random(RANDOM_STATE)
        if cache_mels:
            os.makedirs(CACHE_DIR, exist_ok=True)

    def __len__(self):
        return len(self.filepaths)

    def _load_audio(self, filepath: str) -> np.ndarray:
        y, sr = sf.read(filepath, dtype="float32")
        if sr != SAMPLE_RATE:
            y = librosa.resample(y, orig_sr=sr, target_sr=SAMPLE_RATE)
        return y

    def _mel_for(self, filepath: str) -> np.ndarray:
        """Full-length mel in dB, from the .npy cache when enabled."""
        if not self.cache_mels:
            # No cache: crop the waveform first (exact original behaviour).
            y = fix_length(self._load_audio(filepath), CLIP_SAMPLES, self.train, self.rng)
            return to_mel_db(y)

        cache_path = os.path.join(
            CACHE_DIR, os.path.splitext(os.path.basename(filepath))[0] + ".npy")
        if os.path.exists(cache_path):
            return np.load(cache_path).astype(np.float32)
        mel_db = to_mel_db(self._load_audio(filepath))
        np.save(cache_path, mel_db.astype(np.float16))
        return mel_db

    def __getitem__(self, idx):
        mel_db = fix_frames(self._mel_for(self.filepaths[idx]), self.train, self.rng)
        mel = z_normalize(mel_db)
        image = torch.from_numpy(mel).unsqueeze(0).float()  # (1, 128, 400)
        target = torch.tensor(self.labels[idx], dtype=torch.float32)
        return image, target


def class_weights(labels: np.ndarray) -> dict:
    n_bonafide = (labels == 0).sum()
    n_spoof = (labels == 1).sum()
    total = len(labels)
    return {0: total / (2 * n_bonafide), 1: total / (2 * n_spoof)}


def compute_eer(labels: np.ndarray, scores: np.ndarray) -> float:
    fpr, tpr, _ = roc_curve(labels, scores)
    fnr = 1 - tpr
    idx = np.nanargmin(np.abs(fnr - fpr))
    return float((fpr[idx] + fnr[idx]) / 2)


def run_epoch(model, loader, weights: dict, device, optimizer=None, scaler=None, use_amp=False):
    is_train = optimizer is not None
    model.train(is_train)
    total_loss, all_targets, all_preds = 0.0, [], []

    with torch.set_grad_enabled(is_train):
        for images, targets in loader:
            images = images.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)

            with torch.autocast(device_type=device.type, enabled=use_amp):
                logits = model.forward_logits(images).squeeze(1)
                sample_weights = torch.where(targets == 1, weights[1], weights[0]).to(device)
                loss = nn.functional.binary_cross_entropy_with_logits(
                    logits, targets, weight=sample_weights)

            if is_train:
                optimizer.zero_grad(set_to_none=True)
                if scaler is not None:
                    scaler.scale(loss).backward()
                    scaler.step(optimizer)
                    scaler.update()
                else:
                    loss.backward()
                    optimizer.step()

            total_loss += loss.item() * images.size(0)
            all_targets.append(targets.detach().cpu().numpy())
            all_preds.append(torch.sigmoid(logits.detach().float()).cpu().numpy())

    targets_np = np.concatenate(all_targets)
    preds_np = np.concatenate(all_preds)
    auc = roc_auc_score(targets_np, preds_np)
    eer = compute_eer(targets_np, preds_np)
    return total_loss / len(loader.dataset), auc, eer


def load_manifest(split: str, limit: int = None) -> pd.DataFrame:
    df = pd.read_csv(os.path.join(DATA_DIR, f"{split}_manifest.csv"), encoding="utf-8")
    if limit:
        df = df.sample(min(limit, len(df)), random_state=RANDOM_STATE).reset_index(drop=True)
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--limit", type=int, default=None, help="Cap dataset size per split (debug/smoke runs)")
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--patience", type=int, default=7,
                        help="Stop early after this many epochs without dev EER improvement")
    parser.add_argument("--no-amp", action="store_true", help="Disable mixed-precision training")
    parser.add_argument("--cache-mels", action="store_true",
                        help="Cache full-clip mel spectrograms to data/mel_cache/ (~10 GB disk, "
                             "2-3x faster after the first epoch)")
    args = parser.parse_args()

    torch.manual_seed(RANDOM_STATE)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    use_amp = device.type == "cuda" and not args.no_amp
    if device.type == "cuda":
        torch.backends.cudnn.benchmark = True
    print(f"Using device: {device} (AMP: {'on' if use_amp else 'off'}, "
          f"mel cache: {'on' if args.cache_mels else 'off'})")

    train_df = load_manifest("train", args.limit)
    dev_df = load_manifest("dev", args.limit)
    print(f"Train/dev sizes: {len(train_df)}/{len(dev_df)}")

    weights = {k: torch.tensor(v, dtype=torch.float32, device=device)
               for k, v in class_weights(train_df["label"].to_numpy()).items()}

    loader_kwargs = dict(
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        pin_memory=device.type == "cuda",
        persistent_workers=args.num_workers > 0,
    )
    train_loader = DataLoader(ASVspoofDataset(train_df, train=True, cache_mels=args.cache_mels),
                              shuffle=True, **loader_kwargs)
    dev_loader = DataLoader(ASVspoofDataset(dev_df, train=False, cache_mels=args.cache_mels),
                            shuffle=False, **loader_kwargs)

    model = VoiceSpoofDetector().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    scaler = torch.amp.GradScaler(device.type, enabled=use_amp) if use_amp else None

    best_eer = float("inf")
    epochs_without_improvement = 0
    for epoch in range(1, args.epochs + 1):
        train_loss, train_auc, train_eer = run_epoch(model, train_loader, weights, device,
                                                     optimizer, scaler, use_amp)
        dev_loss, dev_auc, dev_eer = run_epoch(model, dev_loader, weights, device, use_amp=use_amp)
        print(f"Epoch {epoch}/{args.epochs} - train_loss={train_loss:.4f} train_auc={train_auc:.4f} "
              f"train_eer={train_eer:.4f} dev_loss={dev_loss:.4f} dev_auc={dev_auc:.4f} dev_eer={dev_eer:.4f}")

        if dev_eer < best_eer:
            best_eer = dev_eer
            epochs_without_improvement = 0
            torch.save(model.state_dict(), MODEL_PATH)
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= args.patience:
                print(f"Early stopping: no dev EER improvement in {args.patience} epochs")
                break

    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))

    eval_df = load_manifest("eval", args.limit)
    eval_loader = DataLoader(ASVspoofDataset(eval_df, train=False), shuffle=False, **loader_kwargs)
    eval_loss, eval_auc, eval_eer = run_epoch(model, eval_loader, weights, device, use_amp=use_amp)
    print(f"Eval: loss={eval_loss:.4f} auc={eval_auc:.4f} eer={eval_eer:.4f}")

    metrics = {
        "best_dev_eer": best_eer,
        "eval_auc": eval_auc,
        "eval_eer": eval_eer,
        "eval_loss": eval_loss,
        "train_size": len(train_df),
        "dev_size": len(dev_df),
        "eval_size": len(eval_df),
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    os.makedirs(BACKEND_MODELS_DIR, exist_ok=True)
    shutil.copy(MODEL_PATH, os.path.join(BACKEND_MODELS_DIR, "voice_spoof.pth"))
    print(f"Copied {MODEL_PATH} -> {BACKEND_MODELS_DIR}")


if __name__ == "__main__":
    main()
