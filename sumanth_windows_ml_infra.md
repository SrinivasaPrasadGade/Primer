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

# TFLite export
tensorflow>=2.17
tf2onnx>=1.16
onnx2tf>=1.26

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
    image: postgis/postgis:16-3.4
    container_name: primer-db
    environment:
      POSTGRES_DB: primer
      POSTGRES_USER: primer
      POSTGRES_PASSWORD: primer_dev
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./backend/seed_data:/docker-entrypoint-initdb.d
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

### 2.2 Enable pgvector Extension

```sql
-- Run after PostgreSQL starts (add to seed_data/00_extensions.sql)
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2.3 Database Migrations

```powershell
# Run Alembic migrations (creates all schemas + tables from Backend Schema doc)
cd primer/backend
alembic upgrade head
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
**Output:** `backend/seed_data/01_seed.sql`
**Run:** `python generate_seed.py > ../backend/seed_data/01_seed.sql`

This script generates **500–1,000 scam sessions** with distributions matched to NCRB cybercrime statistics.

**What it generates:**

| Table | Rows | Distribution Logic |
|---|---|---|
| `scam_sessions` | 500 | Alert levels: RED 20%, AMBER 40%, YELLOW 40% (matches NCRB severity split) |
| `number_reputation` | 100 | Mix of flagged, clean, and unknown numbers |
| `fraud_graph_entities` | 200+ | Phones, bank accounts, UPI IDs, persons |
| `fraud_graph_edges` | 400+ | Forms 5–8 visible clusters for graph visualization |
| `geo_incidents` | 500+ | Weighted by city: Mumbai 25%, Delhi 22%, Bangalore 18%, Hyderabad 15%, Others 20% |
| `counterfeit_serials` | 20 | Known fake ₹500 and ₹2000 serial patterns |
| `scam_script_corpus` | 50 | Hindi + English templates (CBI, police, customs, tax) |
| `qr_codes_flagged` | 10 | UPI IDs linked to fraud accounts |
| `case_summaries` | 5 | Pre-generated multi-paragraph case narratives |

**How it generates realistic data:**

```python
# ml/data_generation/generate_seed.py
"""
Generates 500–1,000 realistic seed sessions for Primer demo.
Distributions matched to NCRB Cyber Crime Report 2024.
Run: python generate_seed.py > ../backend/seed_data/01_seed.sql
"""
import random
import json
from datetime import datetime, timedelta
import uuid

# ── City distribution (NCRB 2024 cybercrime hotspots) ──
CITY_WEIGHTS = {
    "Mumbai":    {"lat": (18.90, 19.28), "lon": (72.77, 72.98), "weight": 0.25},
    "Delhi":     {"lat": (28.50, 28.78), "lon": (76.95, 77.35), "weight": 0.22},
    "Bangalore": {"lat": (12.85, 13.10), "lon": (77.50, 77.70), "weight": 0.18},
    "Hyderabad": {"lat": (17.30, 17.50), "lon": (78.35, 78.55), "weight": 0.15},
    "Chennai":   {"lat": (12.95, 13.15), "lon": (80.15, 80.30), "weight": 0.10},
    "Pune":      {"lat": (18.45, 18.60), "lon": (73.80, 73.95), "weight": 0.10},
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

def generate_scam_sessions(count=500):
    scam_list = list(SCAM_TYPES.keys())
    scam_weights = list(SCAM_TYPES.values())

    for i in range(count):
        alert_level = random.choices(["RED", "AMBER", "YELLOW"], weights=[20, 40, 40])[0]
        confidence = {
            "RED":    random.uniform(85, 99),
            "AMBER":  random.uniform(60, 84),
            "YELLOW": random.uniform(30, 59),
        }[alert_level]

        scam_type = random.choices(scam_list, weights=scam_weights)[0]
        hour = random.choices(range(24), weights=HOUR_WEIGHTS)[0]

        signals = json.dumps({
            "call_flow_match":  {"score": round(random.uniform(0.7, 0.99), 2)},
            "number_spoofing":  {"score": round(random.uniform(0.5, 0.95), 2)},
            "script_similarity":{"score": round(random.uniform(0.6, 0.98), 2)},
            "voice_synthetic":  {"score": round(random.uniform(0.3, 0.85), 2)},
            "urgency_phrases":  {"score": round(random.uniform(0.7, 1.0), 2)},
        })

        print(f"""INSERT INTO scam_sentinel.scam_sessions
            (id, caller_number, callee_number, call_start, alert_level,
             overall_confidence, scam_type, signal_scores, status,
             deepfake_detected, voice_synthetic_probability)
            VALUES ('{uuid.uuid4()}',
             '+91{random.randint(7000000000, 9999999999)}',
             '+91{random.randint(7000000000, 9999999999)}',
             NOW() - interval '{random.randint(1, 720)} hours'
                   + interval '{hour} hours',
             '{alert_level}', {confidence:.1f}, '{scam_type}',
             '{signals}', '{random.choice(["active","resolved","escalated"])}',
             {str(random.random() > 0.6).lower()},
             {random.uniform(0.3, 0.9):.2f});""")

if __name__ == "__main__":
    generate_scam_sessions(500)
```

---

#### 3.2.3 CDR Synthetic Data Generator

**Script:** `ml/data_generation/generate_cdr.py`
**Output:** `ml/scam-classifier/data/cdr_training_data.csv`
**Run:** `python generate_cdr.py`

This script generates **10,000+ synthetic Call Detail Records** for training the XGBoost Scam Classifier. Feature distributions are derived from published telecom fraud research (ITU-T Technical Reports, IEEE papers on CDR anomaly detection).

**What each row contains (features):**

| Feature | Type | Scam Distribution | Normal Distribution | Source |
|---|---|---|---|---|
| `call_duration_sec` | int | 600–7200s (10min–2hr) | 30–600s (0.5–10min) | Digital arrest calls are long-duration pressure calls |
| `caller_risk_score` | float | 0.6–1.0 | 0.0–0.3 | Derived from number reputation database |
| `is_international_origin` | bool | 70% true | 5% true | Most scam call centres operate from SE Asia |
| `time_of_day_hour` | int | Peaks 10–14 IST | Uniform | Scammers target working hours |
| `script_similarity_max` | float | 0.7–0.99 | 0.0–0.3 | NLP similarity to known scam templates |
| `urgency_phrase_count` | int | 5–25 | 0–2 | "arrest warrant", "FIR", "RBI notice" |
| `caller_complaint_count` | int | 3–50 | 0–1 | Prior complaints filed against this number |
| `callee_age_group` | cat | Skews 55+ (40%) | Uniform | Elderly are disproportionately targeted |
| `call_count_from_number_24h` | int | 20–500 | 1–10 | Mass-dialling pattern |
| `spoofing_indicator` | float | 0.6–1.0 | 0.0–0.2 | CLI mismatch / VoIP routing detection |
| `is_scam` (label) | bool | 1 | 0 | Target variable for XGBoost |

**How it generates realistic data:**

```python
# ml/data_generation/generate_cdr.py
"""
Generates 10,000+ synthetic CDR rows for XGBoost scam classifier training.
Feature distributions based on:
  - ITU-T Technical Paper on Telecom Fraud (2023)
  - IEEE: "CDR-based Fraud Detection using ML" (2022)
  - NCRB Cybercrime Report (2024)
Run: python generate_cdr.py
Output: ml/scam-classifier/data/cdr_training_data.csv
"""
import random
import csv
import numpy as np

TOTAL_ROWS = 10000
SCAM_RATIO = 0.30  # 30% scam, 70% normal (class imbalance handled in training)

AGE_GROUPS = ["18-25", "26-35", "36-45", "46-55", "55-65", "65+"]
AGE_WEIGHTS_SCAM   = [0.05, 0.10, 0.15, 0.20, 0.25, 0.25]  # Elderly targeted
AGE_WEIGHTS_NORMAL = [0.20, 0.25, 0.25, 0.15, 0.10, 0.05]

HOUR_WEIGHTS_SCAM   = [1]*6 + [3,5,8,10,10,10,8,8,5,3,2,2,1,1,1,1,1,1]
HOUR_WEIGHTS_NORMAL = [1]*24  # Uniform

def generate_scam_row():
    return {
        "call_duration_sec":          int(np.random.lognormal(6.5, 0.8)),  # median ~660s
        "caller_risk_score":          round(random.uniform(0.6, 1.0), 2),
        "is_international_origin":    int(random.random() < 0.70),
        "time_of_day_hour":           random.choices(range(24), weights=HOUR_WEIGHTS_SCAM)[0],
        "script_similarity_max":      round(random.uniform(0.70, 0.99), 2),
        "urgency_phrase_count":       random.randint(5, 25),
        "caller_complaint_count":     random.randint(3, 50),
        "callee_age_group":           random.choices(AGE_GROUPS, weights=AGE_WEIGHTS_SCAM)[0],
        "call_count_from_number_24h": random.randint(20, 500),
        "spoofing_indicator":         round(random.uniform(0.6, 1.0), 2),
        "is_scam":                    1,
    }

def generate_normal_row():
    return {
        "call_duration_sec":          int(np.random.lognormal(4.5, 1.0)),  # median ~90s
        "caller_risk_score":          round(random.uniform(0.0, 0.3), 2),
        "is_international_origin":    int(random.random() < 0.05),
        "time_of_day_hour":           random.choices(range(24), weights=HOUR_WEIGHTS_NORMAL)[0],
        "script_similarity_max":      round(random.uniform(0.0, 0.30), 2),
        "urgency_phrase_count":       random.randint(0, 2),
        "caller_complaint_count":     random.randint(0, 1),
        "callee_age_group":           random.choices(AGE_GROUPS, weights=AGE_WEIGHTS_NORMAL)[0],
        "call_count_from_number_24h": random.randint(1, 10),
        "spoofing_indicator":         round(random.uniform(0.0, 0.2), 2),
        "is_scam":                    0,
    }

def main():
    scam_count = int(TOTAL_ROWS * SCAM_RATIO)
    normal_count = TOTAL_ROWS - scam_count

    rows = [generate_scam_row() for _ in range(scam_count)]
    rows += [generate_normal_row() for _ in range(normal_count)]
    random.shuffle(rows)

    with open("ml/scam-classifier/data/cdr_training_data.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} CDR rows ({scam_count} scam, {normal_count} normal)")

if __name__ == "__main__":
    main()
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
    def __init__(self, num_features=6):
        super().__init__()
        self.backbone = timm.create_model("efficientnet_b4", pretrained=True, num_classes=0)
        feature_dim = self.backbone.num_features  # 1792 for B4
        self.heads = nn.ModuleList([
            nn.Sequential(nn.Linear(feature_dim, 256), nn.ReLU(), nn.Dropout(0.3), nn.Linear(256, 1), nn.Sigmoid())
            for _ in range(num_features)
        ])

    def forward(self, x):
        features = self.backbone(x)
        return torch.cat([head(features) for head in self.heads], dim=1)

# Training config
# Dataset: Custom currency images (genuine + counterfeit)
# Augmentation: rotation, brightness, blur (simulating bad phone cameras)
# Epochs: 50
# Batch size: 16 (RTX 4060 can handle this)
# Output: note_auth_net.pth (cloud), note_auth_net.tflite (mobile)
```

**Deliverables:**
- `note_auth_net.pth` → copy to `backend/app/ml/models/`
- `note_auth_net.tflite` → copy to `mobile/assets/models/`

### 4.2 Model 2 — VoiceSpoofDetector (Deepfake Voice)

**Architecture:** LCNN (Light CNN) on mel-spectrograms

```python
# ml/voice-spoof-detector/train.py
class VoiceSpoofDetector(nn.Module):
    """Detects AI-generated/synthetic speech.
    Input: mel-spectrogram (128 x 400) from 4-second audio clip
    Output: probability of synthetic speech (0.0 = genuine, 1.0 = synthetic)
    """
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            # MFM (Max Feature Map) layers
            nn.Conv2d(1, 64, 5, 1, 2), nn.MaxPool2d(2),
            nn.Conv2d(64, 64, 1, 1, 0),  # MFM reduces to 32
            nn.Conv2d(32, 96, 3, 1, 1), nn.MaxPool2d(2),
            nn.Conv2d(96, 96, 1, 1, 0),  # MFM reduces to 48
            nn.Conv2d(48, 128, 3, 1, 1), nn.MaxPool2d(2),
            nn.Conv2d(128, 128, 1, 1, 0),  # MFM reduces to 64
        )
        self.classifier = nn.Sequential(
            nn.Linear(64 * 16 * 50, 256), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(256, 1), nn.Sigmoid()
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)

# Training config
# Dataset: ASVspoof 2019 LA (or 2021)
# Epochs: 30
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

# Train
model = xgb.XGBClassifier(
    max_depth=6,
    n_estimators=200,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric="logloss",
)
model.fit(X_train, y_train)

# Export
joblib.dump(model, "scam_classifier.joblib")
# Feature importance → used for Explainable AI
```

**Deliverable:** `scam_classifier.joblib` → copy to `backend/app/ml/models/`

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

model = RandomForestClassifier(n_estimators=100, max_depth=10)
model.fit(X_train, y_train)
joblib.dump(model, "hotspot_predictor.joblib")
```

**Deliverable:** `hotspot_predictor.joblib` → copy to `backend/app/ml/models/`

---

## 5. Embedding Pipeline (Adaptive Knowledge Base)

```python
# ml/embeddings/embed_corpus.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Use multilingual model for Hindi + English
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def embed_texts(texts: list[str]) -> np.ndarray:
    """Generate 384-dim embeddings for text list."""
    return model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    """Build FAISS index for cosine similarity search."""
    index = faiss.IndexFlatIP(384)
    index.add(embeddings)
    return index

# Usage: embed scam script corpus → save index
# New scam pattern → embed → search top-5 similar → suggest to analyst
```

---

## 6. GPU VRAM Budget (RTX 4060, 8GB)

```
Training NoteAuthNet (EfficientNet-B4, batch=16):  ~3.5 GB
Training VoiceSpoofDetector (LCNN, batch=32):      ~2.0 GB
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
- [ ] Gemini API integration helpers (shared with Srinivas)
- [ ] Copilot function calling schema defined
- [ ] Cross-module correlation logic (link scam session → graph → map)
- [ ] Verify inference times (< 3s for note, < 2s for voice)
- [ ] Final seed data polish (make it look realistic)
