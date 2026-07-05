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

### 3.2 Data Generation Script

```python
# ml/data_generation/generate_seed.py
"""
Generates realistic seed data for Primer demo.
Run: python generate_seed.py > ../backend/seed_data/01_seed.sql
"""
import random
import json
from datetime import datetime, timedelta
import uuid

# Generate 50 scam sessions with realistic signal scores
def generate_scam_sessions():
    scam_types = ["digital_arrest", "cbi_impersonation", "customs_seizure", "tax_evasion"]
    for i in range(50):
        alert_level = random.choices(["RED", "AMBER", "YELLOW"], weights=[10, 20, 20])[0]
        confidence = {"RED": random.uniform(85, 99), "AMBER": random.uniform(60, 84), "YELLOW": random.uniform(30, 59)}[alert_level]

        signals = json.dumps({
            "call_flow_match": {"score": round(random.uniform(0.7, 0.99), 2), "explanation": "Matches digital arrest pattern"},
            "number_spoofing": {"score": round(random.uniform(0.5, 0.95), 2), "explanation": "CLI mismatch detected"},
            "script_similarity": {"score": round(random.uniform(0.6, 0.98), 2), "explanation": f"Matches template #{random.randint(1, 50)}"},
            "voice_synthetic": {"score": round(random.uniform(0.3, 0.85), 2), "explanation": "Spectral analysis complete"},
            "urgency_phrases": {"score": round(random.uniform(0.7, 1.0), 2), "explanation": "Detected: arrest warrant, FIR"},
        })

        print(f"""INSERT INTO scam_sentinel.scam_sessions
            (caller_number, callee_number, call_start, alert_level, overall_confidence,
             scam_type, signal_scores, status, deepfake_detected, voice_synthetic_probability)
            VALUES ('+91{random.randint(7000000000, 9999999999)}', '+91{random.randint(7000000000, 9999999999)}',
             NOW() - interval '{random.randint(1, 72)} hours', '{alert_level}', {confidence:.1f},
             '{random.choice(scam_types)}', '{signals}', 'active',
             {str(random.random() > 0.6).lower()}, {random.uniform(0.3, 0.9):.2f});""")
```

---

## 4. ML Model Training

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
- [ ] Docker Compose: PostgreSQL + PostGIS + pgvector + Redis
- [ ] All database schemas created (run Alembic migrations)
- [ ] pgvector extension enabled
- [ ] Seed data generated (50+ sessions, 100+ entities, 200+ incidents)
- [ ] Seed data loaded and verified
- [ ] `docker compose up` → all healthy on first try

### 2. ML Models Training
- [ ] NoteAuthNet trained → `note_auth_net.pth` + `.tflite`
- [ ] VoiceSpoofDetector trained → `voice_spoof.pth`
- [ ] Scam classifier trained → `scam_classifier.joblib`
- [ ] Hotspot predictor trained → `hotspot_predictor.joblib`

### 3. Agentic Orchestrator & Integration
- [ ] All models copied to `backend/app/ml/models/`
- [ ] TFLite model copied to `mobile/assets/models/`
- [ ] Embedding pipeline for scam corpus
- [ ] FAISS index built for knowledge base
- [ ] Gemini API integration helpers (shared with Srinivas)
- [ ] Copilot function calling schema defined
- [ ] Cross-module correlation logic (link scam session → graph → map)
- [ ] Verify inference times (< 3s for note, < 2s for voice)
- [ ] Final seed data polish (make it look realistic)
