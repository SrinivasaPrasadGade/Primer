# Sumanth — ML & Infrastructure (Windows 11, RTX 4060)

## **Primer — Developer Task Sheet**

| Field | Detail |
|---|---|
| **Owner** | Sumanth |
| **Machine** | OMEN, Windows 11, NVIDIA RTX 4060 (8GB VRAM), 16GB RAM |
| **Role** | Infrastructure setup, ALL ML model training, Agentic Orchestrator |
| **Stack** | Docker, PostgreSQL, Redis, PyTorch, TFLite, scikit-learn, FAISS |
| **Companion Docs** | [TRD](technical_requirements_document.md) · [Backend Schema](backend_schema_document.md) |

---

## 1. Machine Setup

### 1.1 Prerequisites

```powershell
# Install Docker Desktop for Windows
# Download from https://www.docker.com/products/docker-desktop/
# Enable WSL2 backend

# Install Python 3.12
# Download from https://www.python.org/downloads/

# Install CUDA Toolkit 12.x (for PyTorch GPU training)
# Download from https://developer.nvidia.com/cuda-downloads

# Verify GPU
nvidia-smi
# Should show: RTX 4060, 8GB VRAM
```

### 1.2 ML Environment

```powershell
# Create ML training environment
cd primer/ml
python -m venv .venv
.venv\Scripts\activate

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
```

### 1.3 ML requirements.txt

```
# Training
torch>=2.4
torchvision>=0.19
torchaudio>=2.4
timm>=1.0                   # EfficientNet models
albumentations>=1.4         # Image augmentation
scikit-learn>=1.5
xgboost>=2.1
sentence-transformers>=3.0  # IndicBERT embeddings
faiss-cpu>=1.9              # Vector similarity

# Data
pandas>=2.2
numpy>=2.0
pillow>=10.4
librosa>=0.10               # Audio processing
soundfile>=0.12

# Geo (Hotspot Predictor feature fetch)
osmnx>=1.9,<2.0             # OSM ATM/bank density; pinned <2.0, bbox API changed
geopandas>=0.14             # osmnx dependency

# TFLite export
tensorflow>=2.17
tf2onnx>=1.16
onnx2tf>=1.26

# Embedding pipeline (embed_corpus.py reads scam_script_corpus from Postgres)
psycopg2-binary>=2.9

# Utilities
tqdm>=4.66
matplotlib>=3.9
wandb>=0.18                 # Experiment tracking (optional)
joblib>=1.4
```

---

## 2. Infrastructure — Docker Compose

### 2.1 docker-compose.yml (Sumanth owns this file)

```yaml
version: "3.9"

services:
  postgres:
    build: ./postgres   # postgis/postgis:16-3.4 + postgresql-16-pgvector (see postgres/Dockerfile)
    container_name: primer-db
    environment:
      POSTGRES_DB: primer
      POSTGRES_USER: primer
      POSTGRES_PASSWORD: primer_dev
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      # Only the extensions script runs at initdb. 01_seed.sql must NOT be
      # mounted here — initdb scripts run before the backend's Alembic
      # migrations create the tables, so it's loaded manually (see §3.2.2).
      - ./backend/seed_data/00_extensions.sql:/docker-entrypoint-initdb.d/00_extensions.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U primer"]
      interval: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: primer-redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      retries: 5

  backend:
    build: ./backend
    container_name: primer-api
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://primer:primer_dev@postgres:5432/primer
      REDIS_URL: redis://redis:6379
      GEMINI_API_KEY: ${GEMINI_API_KEY}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./uploads:/app/uploads

  dashboard:
    build: ./frontend/dashboard
    container_name: primer-dashboard
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on:
      - backend

volumes:
  pgdata:
```

The custom postgres image exists because the stock `postgis/postgis` image does
not ship pgvector:

```dockerfile
# postgres/Dockerfile
FROM postgis/postgis:16-3.4

RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-16-pgvector \
    && rm -rf /var/lib/apt/lists/*
```

### 2.2 Enable Extensions

```sql
-- seed_data/00_extensions.sql (runs automatically at initdb, see mount above)
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

### 2.3 Database Migrations

The backend container's `entrypoint.sh` runs `alembic upgrade head` automatically
before starting uvicorn, so `docker compose up` creates all schemas/tables on its
own. To run them manually (e.g. before loading seed data without the backend up):

```powershell
# Creates all schemas + tables from the Backend Schema doc
cd primer/backend
alembic upgrade head
# or, via docker:
docker compose run --rm --no-deps --entrypoint alembic backend upgrade head
```

---

## 3. Seed Data

Sumanth creates the seed data that makes the demo look impressive. This is **critical** — empty dashboards = bad demo.

### 3.1 Seed Script: `seed_data/01_seed.sql`

Generate realistic data:

| Data | Count | Notes |
|---|---|---|
| Scam sessions | 50+ | Mix of RED (10), AMBER (20), YELLOW (20) |
| Number reputation entries | 30+ | Include known scam numbers from real NCRP data |
| Fraud graph entities | 100+ | Phones, accounts, UPIs, persons |
| Fraud graph edges | 200+ | Form 3-4 visible clusters |
| Geo incidents | 200+ | Spread across Mumbai, Delhi, Bangalore, Hyderabad |
| Counterfeit serials | 10+ | Known fake ₹500 and ₹2000 serials |
| Scam script corpus | 30+ | Hindi + English templates (CBI, police, customs) |
| QR codes (flagged) | 5+ | UPI IDs linked to fraud accounts |
| Case summaries | 3+ | Pre-generated for demo |
| Knowledge base patterns | 10+ | Various scam types |

### 3.2 Datasets & Data Generation

Data for Primer falls into three categories:

| Category | Purpose | Volume | Source |
|---|---|---|---|
| **ML Training Datasets** | Train the 4 ML models | Thousands–100K+ samples | Public research datasets |
| **Dashboard Seed Data** | Populate demo UI | 500–1,000 sessions | Python generator script (`generate_seed.py`) |
| **CDR Feature Data** | Train Scam Classifier (XGBoost) | 10,000+ rows | Python generator script (`generate_cdr.py`) |

---

#### 3.2.1 ML Training Datasets (Download Links)

**🎤 Voice Spoofing / Deepfake Detection (for VoiceSpoofDetector)**

| Dataset | Size | Link | Notes |
|---|---|---|---|
| ASVspoof 5 (2024) | 2,000+ speakers, 20+ attack types | https://www.asvspoof.org/ | Industry standard; includes adversarial attacks. Download via Zenodo/Hugging Face. |
| ASVspoof 2019 LA | ~25,000 utterances (bonafide + spoofed) | https://datashare.ed.ac.uk/handle/10283/3336 | Lighter alternative; good starting point for LCNN training. |
| TeleAntiFraud-28k | 28,000 audio samples | https://github.com/JunfengChenn/TeleAntiFraud | Telecom-specific fraud audio with transcripts; bridges audio + NLP. |

**💵 Counterfeit Currency Detection (for NoteAuthNet)**

| Dataset | Size | Link | Notes |
|---|---|---|---|
| Indian Currency Note Images 2020 | 4,000+ images, 7 denominations | https://www.kaggle.com/datasets/anmolkumar/indian-currency-note-images-dataset-2020 | ₹10, ₹20, ₹50, ₹100, ₹200, ₹500, ₹2000 notes. |
| Fake Currency Dataset | Real + fake INR images | https://www.kaggle.com/datasets/saathviklekhan/fake-currency-dataset | Labeled real vs counterfeit samples. |
| Currency Dataset (₹500 real+fake) | ₹500 focused | https://www.kaggle.com/datasets/aarya2003/currency-dataset-500-inr-note-real-fake | High-detail for most common denomination. |
| Mendeley Indian Currency | 1,786 images, varied lighting | https://data.mendeley.com/datasets/48ympv8jjf/1 | Good augmentation source with diverse capture conditions. |

**📞 Scam Call / Fraud Detection (for Scam Classifier baseline)**

| Dataset | Size | Link | Notes |
|---|---|---|---|
| Kaggle Fraud Call Detection | Labeled normal vs fraud | https://www.kaggle.com/datasets/narayanyadav/fraud-call-detection | Use as template for CDR feature distributions. |
| UCI SMS Spam Collection | 5,574 SMS messages | https://archive.ics.uci.edu/ml/datasets/sms+spam+collection | Text-based; useful for NLP urgency-phrase training. |

**🗺️ Geo / Crime Hotspot (for Hotspot Predictor baseline)**

| Source | Link | Notes |
|---|---|---|
| NCRB "Crime in India" Reports | https://ncrb.gov.in/crime-in-india.html | District-wise crime statistics; use for realistic city distributions. |
| India Census / OSM | https://www.openstreetmap.org/ | Population density, ATM/bank density for feature engineering. |

---

#### 3.2.2 Dashboard Seed Data Generator

**Script:** `ml/data_generation/generate_seed.py`
**Output:** `backend/seed_data/01_seed.sql` (written directly by the script)
**Run** (AFTER `alembic upgrade head` — the seed references tables and demo users the migration creates):

```powershell
cd ml/data_generation
python generate_seed.py
psql $env:DATABASE_URL -f ..\..\backend\seed_data\01_seed.sql

# Populate geo_intel.predictions — the generator below does not write that table,
# so without this the Geo Intel map reports 0 predicted hotspots. Must run AFTER
# the seed load: the model scores grid points from nearby incident counts, so on an
# unseeded database every point scores low and nothing is stored. Idempotent.
cd ..\..\backend
python -m scripts.bootstrap_predictions
```

This script generates **500 scam sessions** (plus everything below) with distributions matched to NCRB cybercrime statistics.

**What it generates:**

| Table | Rows | Distribution Logic |
|---|---|---|
| `scam_sentinel.scam_sessions` | 500 | Alert levels: RED 20%, AMBER 40%, YELLOW 40% (matches NCRB severity split); call end times peak 10:00–14:00 IST |
| `scam_sentinel.number_reputation` | 100 | Mix of flagged, clean, and unknown numbers |
| `fraud_graph.entities` | ~280 | Phones, bank accounts, UPI IDs, persons, devices, IPs |
| `fraud_graph.edges` | ~500 | Forms 6 visible clusters for graph visualization |
| `geo_intel.incidents` | 550 | Weighted by city: Mumbai 30%, Delhi 26%, Bangalore 22%, Hyderabad 22% (same cities as the cluster names, so map and graph tell one story) |
| `note_verify.counterfeit_serials` | 20 | Known fake ₹500 and ₹2000 serial patterns |
| `scam_sentinel.scam_script_corpus` | 50 | Hindi + English templates (CBI, police, customs, tax), deduped via (template, officer-name) combos |
| `qr_scans.scan_results` | 10 | Flagged/dangerous UPI IDs linked to fraud accounts |
| `core.investigations` + `core.case_summaries` | 5 + 5 | Pre-generated multi-paragraph case narratives |
| `knowledge_base.patterns` | 11 | Verified scam patterns across all major types |

**Cross-module wiring:** 25 RED-alert sessions are also inserted as `phone_number`
entities in the fraud graph (spread round-robin across the 6 clusters) and as
`geo_intel.incidents` rows with `source_ref_id` pointing back at the session — so
the scam session → fraud graph → map correlation path
(`backend/app/services/correlation.py`) has real matches to find during the demo.

**How it generates realistic data** (key excerpts — see the full script for all 9 tables):

```python
# ml/data_generation/generate_seed.py (excerpt)

# ── City distribution (NCRB 2024 cybercrime hotspots; same 4 cities the
#    fraud-graph clusters are named after) ──
CITIES = {
    "Mumbai":    {"lat": (18.90, 19.28), "lon": (72.77, 72.98), "weight": 0.30},
    "Delhi":     {"lat": (28.50, 28.78), "lon": (76.95, 77.35), "weight": 0.26},
    "Bangalore": {"lat": (12.85, 13.10), "lon": (77.50, 77.70), "weight": 0.22},
    "Hyderabad": {"lat": (17.30, 17.50), "lon": (78.35, 78.55), "weight": 0.22},
}

# ── Scam type distribution (NCRB + I4C reports) ──
SCAM_TYPES = {
    "digital_arrest":     0.35,  # Fastest growing; 35% of reported cases
    "cbi_impersonation":  0.25,  # Authority impersonation
    "customs_seizure":    0.20,  # Parcel/courier scam
    "tax_evasion":        0.12,  # IT department threats
    "bank_kyc":           0.08,  # KYC expiry fraud
}

# ── Time distribution (scam calls peak 10am–2pm IST) ──
HOUR_WEIGHTS = [1]*6 + [3,5,8,10,10,10,8,8,5,3,2,2,1,1,1,1,1,1]  # 0–23h

# Per session: anchor on when the call ENDED, pinned to an IST wall-clock hour
# drawn from HOUR_WEIGHTS. days_back >= 1 keeps every call_end strictly in the
# past no matter when the seed is loaded.
days_back = random.randint(1, 30)
hour = random.choices(range(24), weights=HOUR_WEIGHTS)[0]
minute = random.randint(0, 59)
call_end_sql = (
    f"(((NOW() AT TIME ZONE 'Asia/Kolkata')::date"
    f" - interval '{days_back} days'"
    f" + interval '{hour} hours {minute} minutes') AT TIME ZONE 'Asia/Kolkata')"
)
# call_start = call_end - call_duration_sec; alert levels RED/AMBER/YELLOW are
# drawn 20/40/40 with confidence bands 85–99 / 60–84 / 30–59.
```

Other things the real script handles that matter for a clean demo load:
- **Determinism:** `random.seed(42)` — rerunning regenerates the same distributions.
- **Uniqueness:** tracks used `(entity_type, entity_value)` pairs so `fraud_graph.entities`' unique constraint never trips (person names collide easily otherwise).
- **CHECK constraints:** maps `scam_type` → the allowed `geo_intel.incidents.crime_type` values.
- **FK-safe users:** references the demo users (`yashi@primer.demo` etc.) that migration `0001` inserts, via subselects.

---

#### 3.2.3 CDR Synthetic Data Generator

**Script:** `ml/data_generation/generate_cdr.py`
**Output:** `ml/scam-classifier/data/cdr_training_data.csv`
**Run:** `python generate_cdr.py`

This script generates **10,000 synthetic Call Detail Records** for training the XGBoost Scam Classifier. Feature distributions are derived from published telecom fraud research (ITU-T Technical Reports, IEEE papers on CDR anomaly detection).

Distributions are **overlapping** (Beta/Poisson/lognormal with shared support) rather than hard-separated ranges, plus ~6% "hard" rows that mix scam-ish and normal-ish features and 2% label noise — so no single feature perfectly separates the classes and the model must combine signals, like a real CDR fraud classifier.

**What each row contains (features):**

| Feature | Type | Scam Distribution | Normal Distribution | Source |
|---|---|---|---|---|
| `call_duration_sec` | int | lognormal, median ~545s, long tail | lognormal, median ~90s | Digital arrest calls are long-duration pressure calls |
| `caller_risk_score` | float | Beta(6,3), mean ~0.67 | Beta(2,6), mean ~0.25 | Derived from number reputation database |
| `is_international_origin` | bool | 55% true | 12% true | Most scam call centres operate from SE Asia |
| `time_of_day_hour` | int | Peaks 10–14 IST (80/20 blend with uniform) | Uniform (90/10 blend with peaked) | Scammers target working hours |
| `script_similarity_max` | float | Beta(5,3), mean ~0.63 | Beta(2,5), mean ~0.29 | NLP similarity to known scam templates |
| `urgency_phrase_count` | int | Poisson(6) | Poisson(0.8) | "arrest warrant", "FIR", "RBI notice" |
| `caller_complaint_count` | int | Poisson(8) | Poisson(1.2) | Prior complaints filed against this number |
| `callee_age_group` | cat | Skews 55+ (45%) | Roughly uniform | Elderly are disproportionately targeted |
| `call_count_from_number_24h` | int | lognormal, median ~55 | lognormal, median ~5 | Mass-dialling pattern |
| `spoofing_indicator` | float | Beta(5,3) | Beta(2,5) | CLI mismatch / VoIP routing detection |
| `is_scam` (label) | bool | 1 | 0 | Target variable for XGBoost |

**How it generates realistic data** (key excerpts — see the full script):

```python
# ml/data_generation/generate_cdr.py (excerpt)
TOTAL_ROWS = 10000
SCAM_RATIO = 0.30        # 30% scam, 70% normal (handled via scale_pos_weight in training)
HARD_CASE_RATIO = 0.06   # ambiguous rows that blend both distributions
LABEL_NOISE_RATIO = 0.02 # rows where the label is flipped after generation

def generate_scam_row():
    return {
        # lognormal median ~545s, long right tail overlaps short normal calls
        "call_duration_sec": int(np.clip(np.random.lognormal(6.3, 1.0), 15, 7200)),
        "caller_risk_score": _beta_score(6, 3),   # mean ~0.67, tail reaches down to ~0.2
        "is_international_origin": int(random.random() < 0.55),
        "time_of_day_hour": _blend_hour(HOUR_WEIGHTS_SCAM, HOUR_WEIGHTS_NORMAL, mix=0.8),
        "script_similarity_max": _beta_score(5, 3),
        "urgency_phrase_count": int(np.random.poisson(6)),
        "caller_complaint_count": int(np.random.poisson(8)),
        "callee_age_group": random.choices(AGE_GROUPS, weights=AGE_WEIGHTS_SCAM)[0],
        "call_count_from_number_24h": int(np.clip(np.random.lognormal(4.0, 0.9), 1, 800)),
        "spoofing_indicator": _beta_score(5, 3),
        "is_scam": 1,
    }
# generate_normal_row() mirrors this with Beta(2,5-6)/Poisson(~1)/lognormal medians
# ~90s and ~5 calls. generate_hard_case_row() samples each feature independently
# from either distribution, so ~6% of rows don't fit either template cleanly.
```

---

## 4. ML Model Training

> **Run guide:** [ml/TRAINING.md](ml/TRAINING.md) has the exact RTX 4060 commands,
> dataset layouts, and time estimates. The training scripts use mixed precision
> (AMP), parallel data loading, and early stopping by default; VoiceSpoofDetector
> additionally supports `--cache-mels` for a 2-3x speedup after the first epoch.

### 4.1 Model 1 — NoteAuthNet (Counterfeit Currency Detection)

**Architecture:** EfficientNet-B4 with multi-head output (one head per feature)

```python
# ml/note-auth-net/train.py
import torch
import timm
from torch import nn

class NoteAuthNet(nn.Module):
    """Multi-feature currency authentication model.
    Input: 380x380 RGB image of currency note
    Output: 6 feature scores (watermark, thread, microprint, intaglio, colour_shift, overall)
    """
    def __init__(self, num_features=6, pretrained=True):
        super().__init__()
        self.backbone = timm.create_model("efficientnet_b4", pretrained=pretrained, num_classes=0)
        feature_dim = self.backbone.num_features  # 1792 for B4
        # Heads output logits; the loss is BCEWithLogitsLoss (AMP-safe — BCELoss
        # on sigmoid outputs is not). forward() applies sigmoid so inference
        # callers and the ONNX/TFLite export still see probabilities.
        self.heads = nn.ModuleList([
            nn.Sequential(nn.Linear(feature_dim, 256), nn.ReLU(), nn.Dropout(0.3), nn.Linear(256, 1))
            for _ in range(num_features)
        ])

    def forward_logits(self, x):
        features = self.backbone(x)
        return torch.cat([head(features) for head in self.heads], dim=1)

    def forward(self, x):
        return torch.sigmoid(self.forward_logits(x))

# Training config
# Dataset: Custom currency images (genuine + counterfeit), via data/manifest.csv
#          (generate with build_manifest.py). NOTE: only genuine/counterfeit
#          labels exist — all 6 heads train on that shared label (weak
#          supervision); "overall" is the head used for pass/fail.
# Augmentation: rotation, brightness, blur (simulating bad phone cameras)
# Epochs: 50 (early stopping on val AUC, --patience 10)
# Batch size: 8 (fits 8GB RTX 4060 with AMP on Windows; halve on OOM)
# Output: note_auth_net.pth (cloud), note_auth_net.tflite (mobile)
```

**Deliverables:**
- `note_auth_net.pth` → copy to `backend/app/ml/models/`
- `note_auth_net.tflite` → copy to `mobile/assets/models/`

### 4.2 Model 2 — VoiceSpoofDetector (Deepfake Voice)

**Architecture:** LCNN (Light CNN) on mel-spectrograms

```python
# ml/voice-spoof-detector/train.py
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
           (n_fft=400 [25ms @ 16kHz], hop_length=160 [10ms], z-normalized)
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
        # Logits + weighted BCE-with-logits in training (AMP-safe, handles the
        # ~10:1 spoof:bonafide class imbalance); forward() applies sigmoid.
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

# Training config
# Dataset: ASVspoof 2019 LA — uses its own train/dev/eval protocol split
#          (dev for model selection, eval scored once as the reported metric)
# Metric: Equal Error Rate (EER, the standard ASVspoof metric) + ROC-AUC
# Epochs: 30 (early stopping on dev EER, --patience 7)
# Batch size: 32
# Output: voice_spoof.pth
```

**Deliverable:** `voice_spoof.pth` → copy to `backend/app/ml/models/`

### 4.3 Model 3 — Scam Classifier (XGBoost)

**Architecture:** XGBoost on tabular CDR features

```python
# ml/scam-classifier/train.py
import xgboost as xgb
from sklearn.model_selection import train_test_split
import joblib

features = [
    "call_duration_sec",
    "caller_risk_score",
    "is_international_origin",
    "time_of_day_hour",
    "script_similarity_max",
    "urgency_phrase_count",
    "caller_complaint_count",
    "callee_age_group",
    "call_count_from_number_24h",
    "spoofing_indicator",
]

# callee_age_group is a string category — encode it (the fitted LabelEncoder is
# saved alongside the model so the backend encodes inference inputs identically)
age_encoder = LabelEncoder()
df["callee_age_group"] = age_encoder.fit_transform(df["callee_age_group"])

# Train (30/70 class imbalance handled via scale_pos_weight;
# use_label_encoder was removed in xgboost 2.x — don't pass it)
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
model = xgb.XGBClassifier(
    max_depth=6,
    n_estimators=200,
    learning_rate=0.1,
    eval_metric="logloss",
    scale_pos_weight=scale_pos_weight,
    random_state=42,
)
model.fit(X_train, y_train)

# Export
joblib.dump(model, "scam_classifier.joblib")
joblib.dump(age_encoder, "callee_age_group_encoder.joblib")
# Feature importance → feature_importance.json, used for Explainable AI
```

**Deliverables:** `scam_classifier.joblib` + `callee_age_group_encoder.joblib` → copy to `backend/app/ml/models/`

### 4.4 Model 4 — Hotspot Predictor (Random Forest)

```python
# ml/hotspot-predictor/train.py
from sklearn.ensemble import RandomForestClassifier
import joblib

features = [
    "latitude", "longitude",
    "crime_count_7d", "crime_count_30d",
    "population_density",
    "bank_atm_density",
    "day_of_week", "month",
    "avg_loss_amount_area",
]

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    class_weight="balanced",   # hotspot cells are the minority class
    random_state=42,
)
model.fit(X_train, y_train)
joblib.dump(model, "hotspot_predictor.joblib")
# Training data: ml/data_generation/generate_hotspot_data.py (optionally
# enriched with real NCRB CSVs + OSM densities via fetch_geo_features.py)
```

**Deliverable:** `hotspot_predictor.joblib` → copy to `backend/app/ml/models/`

---

## 5. Embedding Pipeline (Adaptive Knowledge Base)

**Script:** `ml/embeddings/embed_corpus.py`
**Input:** `scam_sentinel.scam_script_corpus` rows from PostgreSQL (falls back to
parsing `backend/seed_data/01_seed.sql` if the DB is unreachable)
**Output:**
- `scam_corpus.faiss` — FAISS `IndexFlatIP` (cosine via normalized vectors, 384-dim)
- `scam_corpus_meta.json` — row metadata, position-aligned with the index
- both copied to `backend/app/ml/models/`
- `scam_script_corpus.embedding` — pgvector column updated in place, so the
  backend can also do similarity search in SQL (`embedding <=> $1`)

```python
# ml/embeddings/embed_corpus.py (excerpt)
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Multilingual model for Hindi + English, 384-dim
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
model = SentenceTransformer(EMBED_MODEL)

def embed_texts(model, texts: list[str]) -> np.ndarray:
    """Generate normalized 384-dim embeddings for a text list."""
    return model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    """Cosine similarity search: inner product on normalized vectors."""
    index = faiss.IndexFlatIP(384)
    index.add(embeddings.astype(np.float32))
    return index

# Usage: embed scam script corpus → save index + metadata → write pgvector column
# New scam pattern → embed → search top-5 similar → suggest to analyst
# (interactive check: ml/embeddings/search_corpus.py)
```

```powershell
# Run
docker compose up -d postgres
cd ml/embeddings
python embed_corpus.py
```

---

## 6. GPU VRAM Budget (RTX 4060, 8GB)

```
Training NoteAuthNet (EfficientNet-B4, batch=8, AMP): ~2.5 GB
Training VoiceSpoofDetector (LCNN, batch=32, AMP):    ~2.0 GB
Training XGBoost (CPU, no GPU needed):              ~0 GB
Sentence-Transformers (inference):                  ~1.0 GB
FAISS index (in-memory, CPU):                       ~0 GB
Available for OS:                                   ~1.5 GB

⚠️ Train models ONE AT A TIME. Do not run multiple training jobs.
```

---

## 7. Task Checklist (Phase 1: Sumanth)

### 1. Infrastructure
- [x] Docker Compose: PostgreSQL + PostGIS + pgvector + Redis
- [x] All database schemas created (run Alembic migrations)
- [x] pgvector extension enabled
- [x] Seed data generated (50+ sessions, 100+ entities, 200+ incidents)
- [x] Seed data loaded and verified
- [x] `docker compose up` → all healthy on first try

### 2. ML Models Training
- [x] NoteAuthNet trained → `note_auth_net.pth` + `.tflite` *(run: [ml/TRAINING.md](ml/TRAINING.md) §2)*
- [x] VoiceSpoofDetector trained → `voice_spoof.pth` *(run: [ml/TRAINING.md](ml/TRAINING.md) §3)*
- [x] Scam classifier trained → `scam_classifier.joblib`
- [x] Hotspot predictor trained → `hotspot_predictor.joblib`

### 3. Agentic Orchestrator & Integration
- [x] All models copied to `backend/app/ml/models/`
- [x] TFLite model copied to `mobile/assets/models/`
- [x] Embedding pipeline for scam corpus
- [x] FAISS index built for knowledge base
- [x] Gemini API integration helpers (shared with Srinivas) *(`backend/app/services/gemini_client.py`)*
- [x] Copilot function calling schema defined
- [x] Cross-module correlation logic (link scam session → graph → map)
- [x] Verify inference times (< 3s for note, < 2s for voice) *(run: `python ml/benchmark_inference.py`; note p95 413ms, voice p95 49ms on this machine)*
- [x] Final seed data polish (make it look realistic) *(deduped `scam_script_corpus`, wired 25 RED sessions into the fraud graph + geo map so cross-module correlation has real matches, fixed a call-end-in-the-future bug; verified by loading `01_seed.sql` into a real Postgres)*
- [x] Call times follow the NCRB 10:00–14:00 IST peak *(`HOUR_WEIGHTS` was defined but unused in `generate_seed.py` — call ends were uniform across the day; now pinned to weighted IST wall-clock hours. Regenerated `01_seed.sql` and re-verified by loading into a scratch Postgres DB: 500 sessions, 0 future call ends, 0 acknowledgements before call end, 53% of calls in the 9:00–14:00 IST window, 25 sessions linked to both graph entities and map incidents)*
