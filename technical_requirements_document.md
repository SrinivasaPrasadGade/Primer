# Technical Requirements Document (TRD)

## **Primer — AI-Powered Digital Public Safety Intelligence Platform**

| Field | Detail |
|---|---|
| **Document Version** | 2.0 — Hackathon MVP |
| **Date** | 5 July 2026 |
| **Classification** | Hackathon Submission |
| **Companion Document** | [PRD](product_requirements_document.md) |

---

## 1. Architecture Overview

### 1.1 Design Philosophy — MVP

| Principle | What It Means for MVP |
|---|---|
| **Monolith-first** | Single FastAPI backend with module routers — not 10 microservices |
| **API-first** | All features exposed via REST APIs before UI |
| **Pre-trained models** | Use Gemini API for NLU/summarisation; train only unique models (NoteAuthNet, VoiceSpoofDetector) |
| **Single database** | PostgreSQL for everything; no Neo4j, TimescaleDB, Elasticsearch |
| **Docker Compose** | All services run locally via `docker compose up` — no Kubernetes |

### 1.2 System Architecture

```mermaid
graph TB
    subgraph "Frontend"
        WEB["Web Dashboard<br/>(Next.js)"]
        MOBILE["Citizen Mobile App<br/>(React Native / Expo)"]
    end

    subgraph "API Layer"
        API["FastAPI Backend<br/>(Single Service)<br/>├── /auth<br/>├── /scam-sentinel<br/>├── /note-verify<br/>├── /fraud-graph<br/>├── /geo-intel<br/>├── /citizen-shield<br/>├── /copilot<br/>├── /qr-scan<br/>└── /case-summary"]
    end

    subgraph "AI / ML Layer"
        GEMINI["Gemini API<br/>(Copilot, Summarizer,<br/>Citizen Chat, Script Matching)"]
        CV["NoteAuthNet<br/>(TFLite on-device +<br/>Cloud inference)"]
        VOICE["VoiceSpoofDetector<br/>(LCNN, GPU inference)"]
        EMBED["Sentence Embeddings<br/>(Adaptive KB,<br/>Script Similarity)"]
    end

    subgraph "Data Layer"
        PG["PostgreSQL 16<br/>+ PostGIS"]
        REDIS["Redis 7<br/>(Cache + Sessions)"]
        FILES["Local File Storage<br/>(Evidence, Images)"]
    end

    WEB --> API
    MOBILE --> API
    API --> GEMINI
    API --> CV
    API --> VOICE
    API --> EMBED
    API --> PG
    API --> REDIS
    API --> FILES
```

### 1.3 Simplified vs Production Architecture

| Component | Production | MVP |
|---|---|---|
| Backend | 10+ Go/Python microservices | 1 FastAPI app with routers |
| API Gateway | Kong with rate limiting, JWT plugin | FastAPI middleware |
| Message Queue | Apache Kafka (3 brokers) | Direct function calls / simple Redis pub/sub |
| Primary DB | PostgreSQL 16 (partitioned, replicated) | PostgreSQL 16 (single instance, no partitioning) |
| Graph DB | Neo4j 5.x | PostgreSQL with adjacency tables + recursive CTEs |
| Time-series DB | TimescaleDB | PostgreSQL with timestamp indexes |
| Search Engine | Elasticsearch 8.x | PostgreSQL full-text search (`tsvector`) |
| Vector Store | Weaviate | pgvector extension or in-memory FAISS |
| Object Storage | MinIO (S3-compatible) | Local filesystem (`/uploads/`) |
| Cache | Redis 7 (cluster) | Redis 7 (single instance) |
| Stream Processing | Apache Flink | Python background tasks (asyncio) |
| ML Serving | Triton Inference Server | Direct model loading in FastAPI |
| Monitoring | Prometheus + Grafana + Jaeger | Console logs + basic health endpoints |
| CI/CD | GitHub Actions → K8s | `docker compose up` |

---

## 2. Tech Stack

### 2.1 Backend

| Component | Technology | Why |
|---|---|---|
| **API Framework** | Python FastAPI | Async, fast, auto-generated OpenAPI docs, team knows Python |
| **ORM** | SQLAlchemy 2.0 + asyncpg | Async PostgreSQL access, migration support |
| **Migrations** | Alembic | Standard for SQLAlchemy |
| **Auth** | python-jose (JWT) | Simple JWT tokens, no complex auth library needed |
| **Background Tasks** | FastAPI BackgroundTasks + asyncio | No Celery/Kafka overhead |
| **PDF Generation** | WeasyPrint + Jinja2 | Evidence package / case summary PDFs |
| **WebSocket** | FastAPI WebSocket | Real-time dashboard feed |

### 2.2 Frontend (Web Dashboard)

| Component | Technology | Why |
|---|---|---|
| **Framework** | Next.js 14 (App Router) | React-based, SSR, file-based routing |
| **Styling** | CSS Modules + CSS custom properties | No Tailwind dependency, full control |
| **Charts** | Recharts | Simple, React-native charting |
| **Maps** | Mapbox GL JS | Interactive crime heatmaps |
| **Graph Viz** | Sigma.js + Graphology | Interactive fraud network graphs |
| **Animations** | Framer Motion | Smooth micro-animations |
| **Data Fetching** | SWR | Cache + revalidation |
| **Icons** | Lucide React | Consistent icon set |

### 2.3 Mobile (Citizen App)

| Component | Technology | Why |
|---|---|---|
| **Framework** | React Native / Expo | Single codebase for Android + iOS |
| **Camera** | expo-camera | Note scanning, QR scanning |
| **ML on-device** | TensorFlow Lite (via react-native-tflite) | NoteAuthNet on-device inference |
| **QR Scanning** | expo-barcode-scanner / ML Kit | QR decode + risk check |
| **Navigation** | React Navigation | Standard RN navigation |

### 2.4 AI / ML

| Component | Technology | Why |
|---|---|---|
| **LLM (Copilot, Summarizer, Chat)** | Gemini API (gemini-2.5-flash) | Fast, multimodal, function calling for structured queries |
| **Currency Detection** | EfficientNet-B4 (custom trained) | Multi-feature note analysis |
| **Voice Deepfake** | LCNN on mel-spectrograms | ASVspoof-trained, lightweight |
| **Script Matching** | Sentence-Transformers (multilingual) | IndicBERT embeddings + cosine similarity |
| **Scam Classification** | XGBoost | Fast, explainable, works on tabular CDR features |
| **Hotspot Prediction** | Scikit-learn (Random Forest) | Spatial features, quick to train |
| **Vector Similarity** | FAISS (in-memory) | Adaptive KB similarity search |
| **OCR** | EasyOCR / Tesseract | Serial number extraction from currency |

### 2.5 Infrastructure

| Component | Technology | Why |
|---|---|---|
| **Containers** | Docker + Docker Compose | Simple local dev, single `docker compose up` |
| **Database** | PostgreSQL 16 + PostGIS + pgvector | Relational + spatial + vector in one DB |
| **Cache** | Redis 7 | Session cache, number reputation cache, rate limiting |
| **File Storage** | Local filesystem | `/uploads/evidence/`, `/uploads/images/` |
| **Reverse Proxy** | Nginx (optional) | Only if deploying to a server |

---

## 3. API Specifications

### 3.1 Authentication

```
POST /api/v1/auth/login
  Body: { email, password }
  Response: { access_token, user: { id, name, role, jurisdiction } }

GET  /api/v1/auth/me
  Header: Authorization: Bearer <token>
  Response: { id, name, role, jurisdiction }
```

JWT payload:
```json
{
  "sub": "user-uuid",
  "name": "Yashi",
  "role": "lea_officer",
  "jurisdiction": "mumbai_suburban",
  "exp": 1720000000
}
```

### 3.2 Scam Sentinel

```
GET  /api/v1/scam/sessions                    → List flagged sessions (paginated, filterable)
GET  /api/v1/scam/sessions/{id}               → Session detail + explainable AI breakdown
POST /api/v1/scam/sessions/{id}/acknowledge   → Officer acknowledges alert
GET  /api/v1/scam/numbers/{phone}             → Number reputation lookup
POST /api/v1/scam/numbers/{phone}/flag        → Flag a number manually
GET  /api/v1/scam/stats                       → Dashboard stats

WS   /ws/scam/live                            → Real-time session feed (WebSocket)
```

### 3.3 Note Verify

```
POST /api/v1/note/verify                      → Upload image → get verdict
  Body: { image_base64, denomination_hint? }
  Response: { verdict, confidence, features: [...], serial_number, is_known_counterfeit, annotated_image_url }

GET  /api/v1/note/history                     → Scan history
GET  /api/v1/note/serials/{serial}            → Serial number lookup
GET  /api/v1/note/stats                       → FICN analytics
```

### 3.4 Fraud Graph

```
GET  /api/v1/graph/entity/{type}/{id}         → Entity + connections (2-hop)
GET  /api/v1/graph/cluster/{id}               → Full cluster subgraph
POST /api/v1/graph/search                     → Search entities
GET  /api/v1/graph/path?from={}&to={}         → Shortest path between entities
GET  /api/v1/graph/money-flow/{entity_id}     → Money flow trace
POST /api/v1/graph/dossier/{cluster_id}       → Generate evidence package PDF
```

### 3.5 Geo Intel

```
GET  /api/v1/geo/incidents                    → Incidents list (with lat/lng)
GET  /api/v1/geo/heatmap?bounds={}&type={}    → Aggregated heatmap data
GET  /api/v1/geo/predictions                  → Hotspot predictions (next 7 days)
GET  /api/v1/geo/stats                        → Crime stats by jurisdiction
```

### 3.6 Citizen Shield

```
POST /api/v1/citizen/chat                     → Chat message → AI response
  Body: { message, session_id?, language? }
  Response: { reply, risk_assessment?, suggested_actions? }

GET  /api/v1/citizen/number-check/{phone}     → Public number risk check
```

### 3.7 AI Copilot

```
POST /api/v1/copilot/query
  Body: { question: "Show all complaints linked to UPI xyz@bank" }
  Response: { answer, data: [...], sources: [...], query_executed }
```

### 3.8 QR Scanner

```
POST /api/v1/qr/scan
  Body: { qr_content }
  Response: { risk_level, destination_type, destination_account?, complaint_count, domain_reputation?, explanation }
```

### 3.9 Case Summarizer

```
POST /api/v1/case/summarize
  Body: { evidence_text, complaint_ids? }
  Response: { summary, timeline: [...], suspects: [...], related_complaints: [...], confidence_score }
```

### 3.10 Panic Button

```
POST /api/v1/panic/trigger
  Body: { caller_number, call_details, location?, device_info }
  Response: { report_id, emergency_contact_notified, fraud_report_url }
```

### 3.11 Pre-Answer Call Screening

```
GET  /api/v1/screen/number/{phone}
  Response: { risk_level, risk_score, flags: [...], recommendation }
```

---

## 4. Security (MVP-Appropriate)

| Layer | Implementation |
|---|---|
| **Authentication** | JWT tokens, 24-hour expiry, no refresh tokens (for MVP) |
| **Authorisation** | Role check in middleware — `lea_officer`, `bank_manager`, `citizen` |
| **Data in transit** | HTTPS (self-signed cert for local, Let's Encrypt for deploy) |
| **Data at rest** | PostgreSQL default (no encryption for MVP) |
| **API rate limiting** | Simple Redis-based counter (100 req/min per user) |
| **Input validation** | Pydantic models on all endpoints |
| **CORS** | Configured for dashboard + mobile app origins |

---

## 5. Performance Targets (MVP)

| Metric | Target |
|---|---|
| Dashboard page load | < 2 seconds |
| Scam session detail load | < 500ms |
| Note Verify (on-device) | < 3 seconds |
| Note Verify (cloud) | < 5 seconds |
| QR scan risk check | < 1 second |
| AI Copilot response | < 5 seconds |
| Graph visualisation (100 nodes) | < 2 seconds |
| Pre-answer screening | < 2 seconds |
| Number reputation lookup | < 200ms (Redis cache) |

---

## 6. Deployment (MVP)

```
# Everything starts with one command:
docker compose up -d

# Services:
#   postgres:5432    — database
#   redis:6379       — cache
#   backend:8000     — FastAPI backend
#   dashboard:3000   — Next.js web dashboard

# Mobile app:
cd mobile && npx expo start
```

### docker-compose.yml structure:
```yaml
services:
  postgres:
    image: postgis/postgis:16-3.4
    environment:
      POSTGRES_DB: primer
      POSTGRES_USER: primer
      POSTGRES_PASSWORD: primer_dev
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: postgresql+asyncpg://primer:primer_dev@postgres:5432/primer
      REDIS_URL: redis://redis:6379
      GEMINI_API_KEY: ${GEMINI_API_KEY}
    depends_on: [postgres, redis]

  dashboard:
    build: ./frontend/dashboard
    ports: ["3000:3000"]
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on: [backend]

volumes:
  pgdata:
```
