# Training the Primer ML Models (RTX 4060, 8GB VRAM)

Completes stages **4.1 (NoteAuthNet)** and **4.2 (VoiceSpoofDetector)** from
[sumanth_windows_ml_infra.md](../sumanth_windows_ml_infra.md). Stages 4.3 and
4.4 (Scam Classifier, Hotspot Predictor) are already trained and deployed.

Both training scripts are tuned for the RTX 4060:

| Optimization | Effect |
|---|---|
| Mixed precision (AMP), on by default | ~1.7-2x faster, ~40% less VRAM |
| `channels_last` + cuDNN autotune (NoteAuthNet) | faster EfficientNet convs |
| 4 DataLoader workers + pinned memory (default) | GPU no longer waits on disk |
| `--cache-mels` (VoiceSpoofDetector) | 2-3x faster after epoch 1 (~10 GB disk) |
| Early stopping (`--patience`) | run usually ends well before max epochs |

**Expected wall-clock on the OMEN (RTX 4060):**

| Model | Old estimate | With optimizations |
|---|---|---|
| NoteAuthNet (≤50 epochs, batch 16) | 2-2.5 h | **~45-75 min** (early stop typically 25-35 epochs) |
| VoiceSpoofDetector (≤30 epochs, batch 32, cached mels) | 1.5-2 h | **~30-50 min** |

Train **one model at a time** (8 GB VRAM budget, see section 6 of the task sheet).

---

## 0. One-time setup

```powershell
cd primer\ml
python -m venv .venv
.venv\Scripts\activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt

# Sanity check — must print True
python -c "import torch; print(torch.cuda.is_available())"
```

## 1. Datasets (once)

Both raw datasets live under `primer\data\raw\` (gitignored — never commit them).

**Currency (NoteAuthNet):** download from Kaggle
(e.g. https://www.kaggle.com/datasets/saathviklekhan/fake-currency-dataset)
and extract so images land at:

```
data\raw\currency\currency dataset 1.1\data\data\real\<denomination>\*.jpg
data\raw\currency\currency dataset 1.1\data\data\fake\<denomination>\*.jpg
```

**ASVspoof 2019 LA (VoiceSpoofDetector):** download `LA.zip` (~7 GB) from
https://datashare.ed.ac.uk/handle/10283/3336 and extract to:

```
data\raw\voice_spoofing\ASVspoof 2019\LA\ASVspoof2019_LA_cm_protocols\...
data\raw\voice_spoofing\ASVspoof 2019\LA\ASVspoof2019_LA_{train,dev,eval}\flac\*.flac
```

## 2. Train NoteAuthNet (stage 4.1)

```powershell
cd primer\ml\note-auth-net
python build_manifest.py
python train.py --epochs 50 --batch-size 16
```

- If you hit `CUDA out of memory`: drop to `--batch-size 8`.
- The TFLite export at the end needs the TensorFlow/onnx2tf deps from
  `requirements.txt` and takes ~5-10 min on CPU. To defer it, add
  `--skip-tflite-export` and re-run the export later.
- Outputs are copied automatically to `backend/app/ml/models/note_auth_net.pth`
  and `mobile/assets/models/note_auth_net.tflite`.

**Quick smoke test first (2 min, recommended):**
`python train.py --epochs 1 --limit 40 --num-workers 0 --skip-tflite-export`

## 3. Train VoiceSpoofDetector (stage 4.2)

```powershell
cd primer\ml\voice-spoof-detector
python build_manifest.py
python train.py --epochs 30 --batch-size 32 --cache-mels
```

- `--cache-mels` writes ~10 GB of `.npy` files to `data/mel_cache/` on the
  first epoch; every later epoch skips FLAC decoding entirely. Omit it if
  disk is tight. Delete `data/mel_cache/` afterwards to reclaim the space.
- Output is copied automatically to `backend/app/ml/models/voice_spoof.pth`.

**Quick smoke test first:**
`python train.py --epochs 1 --limit 64 --num-workers 0`

## 4. Embedding pipeline + FAISS index (section 5)

```powershell
docker compose up -d postgres        # corpus lives in scam_sentinel.scam_script_corpus
cd primer\ml\embeddings
python embed_corpus.py
```

Writes `scam_corpus.faiss` + `scam_corpus_meta.json` and copies both to
`backend/app/ml/models/`.

## 5. Verify + commit

```powershell
dir ..\..\backend\app\ml\models
# expect: note_auth_net.pth, voice_spoof.pth, scam_classifier.joblib,
#         hotspot_predictor.joblib, callee_age_group_encoder.joblib,
#         scam_corpus.faiss, scam_corpus_meta.json
dir ..\..\mobile\assets\models
# expect: note_auth_net.tflite

git add backend/app/ml/models mobile/assets/models ml/*/metrics.json
git commit -m "Train NoteAuthNet + VoiceSpoofDetector, build KB embeddings (4.1, 4.2, 5)"
git push
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| `CUDA out of memory` | halve `--batch-size`; AMP is already on |
| Loss becomes `nan` | rerun with `--no-amp` (rare on Ada GPUs) |
| DataLoader crashes on Windows | use `--num-workers 0` (slower but reliable) |
| GPU utilization low during voice training | add `--cache-mels`, raise `--num-workers` to 6-8 |
| `FileNotFoundError` from build_manifest | dataset extracted to the wrong path — compare against section 1 layouts exactly |
