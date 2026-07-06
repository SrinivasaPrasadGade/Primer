"""
Trains NoteAuthNet (EfficientNet-B4, multi-head) on the currency image dataset.

Input:  ml/note-auth-net/data/manifest.csv
         (generate with ml/note-auth-net/build_manifest.py)
Output: ml/note-auth-net/note_auth_net.pth
         (copied to backend/app/ml/models/note_auth_net.pth)
        ml/note-auth-net/note_auth_net.tflite
         (copied to mobile/assets/models/note_auth_net.tflite)

The raw dataset only labels each note image genuine/counterfeit — there is no
per-feature ground truth for watermark/thread/microprint/intaglio/colour_shift.
All 6 heads are therefore trained against the same genuine/counterfeit label
(weak supervision). The "overall" head is the one used for the pass/fail
decision; the other 5 heads currently learn a correlated but not independently
verified signal, and should be replaced with real per-feature labels
(e.g. crops from the *_Features datasets, hand-annotated) before this model is
trusted to explain *why* a note failed rather than just whether it did.

Performance (tuned for RTX 4060, 8GB VRAM):
  - Mixed precision (AMP) is on by default on CUDA — roughly halves VRAM and
    step time on Ampere/Ada GPUs. Disable with --no-amp if you see NaNs.
  - Heads output logits and the loss is BCEWithLogitsLoss (AMP-safe; BCELoss
    on sigmoid outputs is not). forward() still applies sigmoid, so inference
    callers and the ONNX/TFLite export see probabilities as before, and
    checkpoints remain key-compatible with the previous Sigmoid-in-Sequential
    layout (Sigmoid held no parameters).
  - channels_last memory format speeds up EfficientNet convs under AMP.
  - Early stopping (--patience) ends the run when val AUC stops improving.

Run (defaults are tuned for an 8GB RTX 4060 on Windows — no flags needed):
    cd ml/note-auth-net
    python train.py
"""
import argparse
import json
import os
import shutil

import albumentations as A
import numpy as np
import pandas as pd
import timm
import torch
from albumentations.pytorch import ToTensorV2
from PIL import Image
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, Dataset

RANDOM_STATE = 42
IMG_SIZE = 380
# On Windows, DataLoader workers are spawned processes that each re-import
# torch and reload the full CUDA DLL stack (~2-3 GB of committed memory per
# worker). On machines with a modest pagefile that fails with
# "OSError: [WinError 1455] The paging file is too small". Default to 0
# workers on Windows (in-process loading — reliable, a bit slower); pass
# --num-workers 2..4 only after enlarging the pagefile.
DEFAULT_NUM_WORKERS = 0 if os.name == "nt" else 4
# Some source images are raw high-DPI scans (tens of megapixels). Downsize
# before the NumPy conversion below so a handful of oversized files don't
# blow up per-worker memory while waiting for Albumentations' own Resize.
MAX_RAW_DIM = 800
FEATURE_NAMES = ["watermark", "thread", "microprint", "intaglio", "colour_shift", "overall"]
OVERALL_IDX = FEATURE_NAMES.index("overall")

BASE_DIR = os.path.dirname(__file__)
MANIFEST_PATH = os.path.join(BASE_DIR, "data", "manifest.csv")
MODEL_PATH = os.path.join(BASE_DIR, "note_auth_net.pth")
TFLITE_PATH = os.path.join(BASE_DIR, "note_auth_net.tflite")
METRICS_PATH = os.path.join(BASE_DIR, "metrics.json")
BACKEND_MODELS_DIR = os.path.join(BASE_DIR, "..", "..", "backend", "app", "ml", "models")
MOBILE_MODELS_DIR = os.path.join(BASE_DIR, "..", "..", "mobile", "assets", "models")

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


class NoteAuthNet(nn.Module):
    """Multi-feature currency authentication model.
    Input: 380x380 RGB image of currency note
    Output: 6 feature scores (watermark, thread, microprint, intaglio, colour_shift, overall)
    """
    def __init__(self, num_features=6, pretrained=True):
        super().__init__()
        self.backbone = timm.create_model("efficientnet_b4", pretrained=pretrained, num_classes=0)
        feature_dim = self.backbone.num_features  # 1792 for B4
        self.heads = nn.ModuleList([
            nn.Sequential(nn.Linear(feature_dim, 256), nn.ReLU(), nn.Dropout(0.3), nn.Linear(256, 1))
            for _ in range(num_features)
        ])

    def forward_logits(self, x):
        features = self.backbone(x)
        return torch.cat([head(features) for head in self.heads], dim=1)

    def forward(self, x):
        return torch.sigmoid(self.forward_logits(x))


class CurrencyDataset(Dataset):
    def __init__(self, df: pd.DataFrame, transform: A.Compose):
        self.filepaths = df["filepath"].tolist()
        self.labels = df["label"].astype("float32").to_numpy()
        self.transform = transform

    def __len__(self):
        return len(self.filepaths)

    def __getitem__(self, idx):
        with Image.open(self.filepaths[idx]) as raw:
            # For JPEGs, ask libjpeg to decode at a reduced scale directly
            # (cheaper than a full decode + separate downsize). No-op for
            # other formats.
            raw.draft("RGB", (MAX_RAW_DIM, MAX_RAW_DIM))
            image = raw.convert("RGB")
        if image.width > MAX_RAW_DIM or image.height > MAX_RAW_DIM:
            image.thumbnail((MAX_RAW_DIM, MAX_RAW_DIM), Image.BILINEAR)
        image = self.transform(image=np.array(image))["image"]
        # Weak supervision: every head shares the genuine/counterfeit label
        # (see module docstring — no per-feature ground truth exists yet).
        target = torch.full((len(FEATURE_NAMES),), self.labels[idx], dtype=torch.float32)
        return image, target


def build_transforms(img_size: int):
    train_tf = A.Compose([
        A.Resize(img_size, img_size),
        A.Rotate(limit=15, p=0.5),
        A.RandomBrightnessContrast(p=0.5),
        A.GaussianBlur(blur_limit=(3, 5), p=0.3),
        A.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ToTensorV2(),
    ])
    eval_tf = A.Compose([
        A.Resize(img_size, img_size),
        A.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ToTensorV2(),
    ])
    return train_tf, eval_tf


def load_splits(limit: int = None):
    df = pd.read_csv(MANIFEST_PATH, encoding="utf-8")
    if limit and limit < len(df):
        df, _ = train_test_split(df, train_size=limit, stratify=df["label"], random_state=RANDOM_STATE)

    def stratify_key(frame: pd.DataFrame) -> pd.Series:
        key = frame["denomination"].astype(str) + "_" + frame["label"].astype(str)
        # Fall back to the coarser label-only split if any (denom, label) group is
        # too small to stratify on (happens with small --limit smoke runs).
        if key.value_counts().min() < 2:
            return frame["label"].astype(str)
        return key

    train_df, temp_df = train_test_split(df, test_size=0.3, stratify=stratify_key(df), random_state=RANDOM_STATE)
    val_df, test_df = train_test_split(temp_df, test_size=0.5, stratify=stratify_key(temp_df), random_state=RANDOM_STATE)
    return train_df.reset_index(drop=True), val_df.reset_index(drop=True), test_df.reset_index(drop=True)


def run_epoch(model, loader, criterion, device, optimizer=None, scaler=None, use_amp=False):
    is_train = optimizer is not None
    model.train(is_train)
    total_loss, all_targets, all_preds = 0.0, [], []

    with torch.set_grad_enabled(is_train):
        for images, targets in loader:
            images = images.to(device, non_blocking=True).to(memory_format=torch.channels_last)
            targets = targets.to(device, non_blocking=True)

            with torch.autocast(device_type=device.type, enabled=use_amp):
                logits = model.forward_logits(images)
                loss = criterion(logits, targets)

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
            probs = torch.sigmoid(logits[:, OVERALL_IDX].detach().float())
            all_targets.append(targets[:, OVERALL_IDX].detach().cpu().numpy())
            all_preds.append(probs.cpu().numpy())

    targets_np = np.concatenate(all_targets)
    preds_np = np.concatenate(all_preds)
    auc = roc_auc_score(targets_np, preds_np) if len(np.unique(targets_np)) > 1 else float("nan")
    return total_loss / len(loader.dataset), auc


def export_tflite(model: nn.Module, img_size: int, device):
    """Trace the trained model through ONNX -> TF SavedModel -> TFLite."""
    import onnx2tf
    import tempfile

    model.eval().to("cpu")
    dummy_input = torch.randn(1, 3, img_size, img_size)
    onnx_path = os.path.join(BASE_DIR, "note_auth_net.onnx")
    torch.onnx.export(
        model, dummy_input, onnx_path,
        input_names=["image"], output_names=["scores"],
        opset_version=17, dynamo=False,
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        onnx2tf.convert(
            input_onnx_file_path=onnx_path,
            output_folder_path=tmp_dir,
            output_integer_quantized_tflite=False,
            non_verbose=True,
        )
        produced = [f for f in os.listdir(tmp_dir) if f.endswith(".tflite")]
        if not produced:
            raise RuntimeError("onnx2tf did not produce a .tflite file")
        # Prefer the plain float32 export if multiple variants were produced.
        chosen = next((f for f in produced if "float32" in f), produced[0])
        shutil.copy(os.path.join(tmp_dir, chosen), TFLITE_PATH)

    model.to(device)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=8,
                        help="8 fits an 8GB RTX 4060 on Windows; halve it on CUDA OOM")
    parser.add_argument("--img-size", type=int, default=IMG_SIZE)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--limit", type=int, default=None, help="Cap dataset size (debug/smoke runs)")
    parser.add_argument("--num-workers", type=int, default=DEFAULT_NUM_WORKERS,
                        help="DataLoader worker processes (default 0 on Windows — see note at top)")
    parser.add_argument("--patience", type=int, default=10,
                        help="Stop early after this many epochs without val AUC improvement")
    parser.add_argument("--no-amp", action="store_true", help="Disable mixed-precision training")
    parser.add_argument("--no-pretrained", action="store_true",
                        help="Skip the ImageNet weight download (offline smoke runs only — "
                             "real training should always start from pretrained weights)")
    parser.add_argument("--skip-tflite-export", action="store_true")
    args = parser.parse_args()

    torch.manual_seed(RANDOM_STATE)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    use_amp = device.type == "cuda" and not args.no_amp
    if device.type == "cuda":
        torch.backends.cudnn.benchmark = True
    print(f"Using device: {device} (AMP: {'on' if use_amp else 'off'})")

    train_df, val_df, test_df = load_splits(limit=args.limit)
    print(f"Train/val/test sizes: {len(train_df)}/{len(val_df)}/{len(test_df)}")

    loader_kwargs = dict(
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        pin_memory=device.type == "cuda",
        persistent_workers=args.num_workers > 0,
    )
    train_tf, eval_tf = build_transforms(args.img_size)
    train_loader = DataLoader(CurrencyDataset(train_df, train_tf), shuffle=True, **loader_kwargs)
    val_loader = DataLoader(CurrencyDataset(val_df, eval_tf), shuffle=False, **loader_kwargs)
    test_loader = DataLoader(CurrencyDataset(test_df, eval_tf), shuffle=False, **loader_kwargs)

    model = NoteAuthNet(num_features=len(FEATURE_NAMES), pretrained=not args.no_pretrained).to(device)
    model = model.to(memory_format=torch.channels_last)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    scaler = torch.amp.GradScaler(device.type, enabled=use_amp) if use_amp else None

    best_val_auc = -1.0
    epochs_without_improvement = 0
    for epoch in range(1, args.epochs + 1):
        train_loss, train_auc = run_epoch(model, train_loader, criterion, device, optimizer, scaler, use_amp)
        val_loss, val_auc = run_epoch(model, val_loader, criterion, device, use_amp=use_amp)
        print(f"Epoch {epoch}/{args.epochs} - train_loss={train_loss:.4f} train_auc={train_auc:.4f} "
              f"val_loss={val_loss:.4f} val_auc={val_auc:.4f}")

        if val_auc > best_val_auc:
            best_val_auc = val_auc
            epochs_without_improvement = 0
            torch.save(model.state_dict(), MODEL_PATH)
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= args.patience:
                print(f"Early stopping: no val AUC improvement in {args.patience} epochs")
                break

    model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
    test_loss, test_auc = run_epoch(model, test_loader, criterion, device, use_amp=use_amp)
    print(f"Test: loss={test_loss:.4f} auc={test_auc:.4f}")

    metrics = {
        "feature_names": FEATURE_NAMES,
        "best_val_auc": best_val_auc,
        "test_auc": test_auc,
        "test_loss": test_loss,
        "train_size": len(train_df),
        "val_size": len(val_df),
        "test_size": len(test_df),
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    os.makedirs(BACKEND_MODELS_DIR, exist_ok=True)
    shutil.copy(MODEL_PATH, os.path.join(BACKEND_MODELS_DIR, "note_auth_net.pth"))
    print(f"Copied {MODEL_PATH} -> {BACKEND_MODELS_DIR}")

    if not args.skip_tflite_export:
        # The trained .pth is already saved and copied at this point. Never let
        # an export failure (TF loads its own multi-GB DLL stack, which can hit
        # the same Windows pagefile limit) read as a failed training run.
        try:
            export_tflite(model, args.img_size, device)
            os.makedirs(MOBILE_MODELS_DIR, exist_ok=True)
            shutil.copy(TFLITE_PATH, os.path.join(MOBILE_MODELS_DIR, "note_auth_net.tflite"))
            print(f"Copied {TFLITE_PATH} -> {MOBILE_MODELS_DIR}")
        except Exception as exc:  # noqa: BLE001
            print(f"\nTFLite export FAILED ({type(exc).__name__}: {exc})")
            print("Training itself succeeded — note_auth_net.pth is saved and copied to the "
                  "backend. Re-run the export later with:\n"
                  "    python export_tflite.py")

    print("\nDone. Trained model: note_auth_net.pth (copied to backend/app/ml/models/)")


if __name__ == "__main__":
    main()
