"""
Re-runs the TFLite export from an already-trained note_auth_net.pth, without
retraining. Use this if train.py finished but its export step failed (e.g. the
TensorFlow DLLs hit the Windows pagefile limit — close other apps first).

Run:
    cd ml/note-auth-net
    python export_tflite.py
"""
import argparse
import os
import shutil

import torch

from train import IMG_SIZE, MODEL_PATH, TFLITE_PATH, MOBILE_MODELS_DIR, NoteAuthNet, export_tflite


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--img-size", type=int, default=IMG_SIZE)
    args = parser.parse_args()

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"{MODEL_PATH} not found — run train.py first")

    model = NoteAuthNet(pretrained=False)
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu", weights_only=True))
    model.eval()

    export_tflite(model, args.img_size, torch.device("cpu"))
    os.makedirs(MOBILE_MODELS_DIR, exist_ok=True)
    shutil.copy(TFLITE_PATH, os.path.join(MOBILE_MODELS_DIR, "note_auth_net.tflite"))
    print(f"Exported {TFLITE_PATH} and copied it to {MOBILE_MODELS_DIR}")


if __name__ == "__main__":
    main()
