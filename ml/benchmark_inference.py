"""
Verifies the two latency budgets from technical_requirements_document.md §5:

    Note Verify (on-device)  < 3 seconds   (NoteAuthNet, note_auth_net.tflite)
    Pre-answer screening     < 2 seconds   (VoiceSpoofDetector, voice_spoof.pth)

Each model is timed end-to-end (preprocessing + inference, batch size 1 — the
real usage pattern: one note scan, one incoming call) on real held-out
samples, matching the deployment target for each model:
  - NoteAuthNet runs on-device via TFLite -> benchmarked on CPU (XNNPACK),
    the same backend the mobile TFLite runtime uses.
  - VoiceSpoofDetector runs server-side as part of call screening -> the
    docker-compose backend has no GPU passthrough, so it's benchmarked on
    CPU (the actual deployment target), not the RTX 4060 used for training.

Run:
    cd ml
    python benchmark_inference.py
"""
import os
import statistics
import sys
import time

import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
NOTE_DIR = os.path.join(BASE_DIR, "note-auth-net")
VOICE_DIR = os.path.join(BASE_DIR, "voice-spoof-detector")

NOTE_TARGET_S = 3.0
VOICE_TARGET_S = 2.0
N_SAMPLES = 10
N_WARMUP = 2


def percentile(values, pct):
    values = sorted(values)
    idx = min(len(values) - 1, int(round(pct / 100 * (len(values) - 1))))
    return values[idx]


def report(name, target_s, timings_s):
    mean_s = statistics.mean(timings_s)
    p95_s = percentile(timings_s, 95)
    worst_s = max(timings_s)
    passed = p95_s < target_s
    print(f"\n{name}")
    print(f"  samples: {len(timings_s)}   mean: {mean_s*1000:.0f} ms   "
          f"p95: {p95_s*1000:.0f} ms   worst: {worst_s*1000:.0f} ms   target: < {target_s*1000:.0f} ms")
    print(f"  {'PASS' if passed else 'FAIL'} (gate: p95 < target)")
    return passed


def bench_note_auth_net():
    import tensorflow as tf
    from PIL import Image

    manifest = pd.read_csv(os.path.join(NOTE_DIR, "data", "manifest.csv"))
    samples = manifest.sample(n=min(N_SAMPLES, len(manifest)), random_state=42)["filepath"].tolist()

    tflite_path = os.path.join(NOTE_DIR, "note_auth_net.tflite")
    if not os.path.exists(tflite_path):
        print(f"SKIP NoteAuthNet: {tflite_path} not found — run ml/note-auth-net/train.py or export_tflite.py")
        return None

    interpreter = tf.lite.Interpreter(model_path=tflite_path, num_threads=1)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]
    img_size = input_details["shape"][1]
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    def preprocess_and_infer(filepath):
        start = time.perf_counter()
        with Image.open(filepath) as raw:
            image = raw.convert("RGB").resize((img_size, img_size), Image.BILINEAR)
        arr = (np.asarray(image, dtype=np.float32) / 255.0 - mean) / std
        arr = arr[np.newaxis, ...].astype(np.float32)  # NHWC, matches tflite input
        interpreter.set_tensor(input_details["index"], arr)
        interpreter.invoke()
        _ = interpreter.get_tensor(output_details["index"])
        return time.perf_counter() - start

    for filepath in samples[:N_WARMUP]:
        preprocess_and_infer(filepath)

    timings = [preprocess_and_infer(f) for f in samples]
    return report("NoteAuthNet (on-device TFLite, note scan)", NOTE_TARGET_S, timings)


def bench_voice_spoof_detector():
    import torch

    sys.path.insert(0, VOICE_DIR)
    from train import (VoiceSpoofDetector, CLIP_SAMPLES, fix_length, fix_frames,
                        to_mel_db, z_normalize, MODEL_PATH, RANDOM_STATE, SAMPLE_RATE)
    import random
    import librosa
    import soundfile as sf

    eval_manifest_path = os.path.join(VOICE_DIR, "data", "eval_manifest.csv")
    if not os.path.exists(MODEL_PATH) or not os.path.exists(eval_manifest_path):
        print(f"SKIP VoiceSpoofDetector: missing {MODEL_PATH} or {eval_manifest_path}")
        return None

    manifest = pd.read_csv(eval_manifest_path)
    samples = manifest.sample(n=min(N_SAMPLES, len(manifest)), random_state=42)["filepath"].tolist()
    missing = [f for f in samples if not os.path.exists(f)]
    if missing:
        print(f"SKIP VoiceSpoofDetector: {len(missing)} eval clip(s) not found locally "
              f"(raw dataset not downloaded) — see ml/TRAINING.md §1")
        return None

    device = torch.device("cpu")  # matches the GPU-less docker-compose backend
    model = VoiceSpoofDetector().to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
    model.eval()
    rng = random.Random(RANDOM_STATE)

    def preprocess_and_infer(filepath):
        start = time.perf_counter()
        y, sr = sf.read(filepath, dtype="float32")
        if sr != SAMPLE_RATE:
            y = librosa.resample(y, orig_sr=sr, target_sr=SAMPLE_RATE)
        y = fix_length(y, CLIP_SAMPLES, train=False, rng=rng)
        mel_db = fix_frames(to_mel_db(y), train=False, rng=rng)
        mel = z_normalize(mel_db)
        image = torch.from_numpy(mel).unsqueeze(0).unsqueeze(0).float().to(device)
        with torch.no_grad():
            _ = model(image)
        return time.perf_counter() - start

    for filepath in samples[:N_WARMUP]:
        preprocess_and_infer(filepath)

    timings = [preprocess_and_infer(f) for f in samples]
    return report("VoiceSpoofDetector (server-side CPU, pre-answer screening)", VOICE_TARGET_S, timings)


def main():
    results = [bench_note_auth_net(), bench_voice_spoof_detector()]
    ran = [r for r in results if r is not None]
    if not ran:
        print("\nNo benchmarks ran — see SKIP reasons above.")
        sys.exit(1)
    if all(ran):
        print("\nAll inference-time budgets met.")
        sys.exit(0)
    print("\nOne or more inference-time budgets were NOT met.")
    sys.exit(1)


if __name__ == "__main__":
    main()
