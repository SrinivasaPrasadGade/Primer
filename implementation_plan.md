# Implementation Plan

## **Primer — AI-Powered Digital Public Safety Intelligence Platform**

| Field | Detail |
|---|---|
| **Document Version** | 2.0 — Hackathon MVP |
| **Date** | 5 July 2026 |
| **Total Duration** | ~3 weeks (hackathon sprint) |
| **Team** | 4 people |
| **Companion Docs** | PRD · TRD · App Flow · Backend Schema · UI/UX Design |

---

## Quick Summary

```
Primer MVP = 5 modules + 8 extra features + 1 unified backend

┌─────────────────────────────────────────────────────────────────┐
│  CORE MODULES                                                    │
│  M1: Scam Sentinel    — Live scam detection + Explainable AI    │
│  M2: Note Verify      — Camera-based counterfeit scanner        │
│  M3: Fraud Graph      — Interactive fraud network graph         │
│  M4: Geo Intel        — Crime heatmap + hotspot prediction      │
│  M5: Citizen Shield   — AI chatbot for citizens                 │
│                                                                   │
│  EXTRA FEATURES                                                  │
│  F6:  AI Investigation Copilot    F10: AI Case Summarizer       │
│  F7:  QR Code Scanner             F11: Adaptive Fraud KB        │
│  F8:  Deepfake Voice Detector     F12: Panic Button (SOS)       │
│  F9:  Explainable AI              F13: Pre-Answer Screening     │
├─────────────────────────────────────────────────────────────────┤
│  STACK: FastAPI + PostgreSQL + Redis + Next.js + React Native   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Team Structure (4 People)

| Person | Machine | Responsibilities |
|---|---|---|
| **Sumanth** | Windows 11, OMEN, RTX 4060 | Infrastructure (Docker, DBs), ALL ML model training, Agentic Orchestrator |
| **Srinivas** | Mac M3 Air, 8GB | Core backend: Auth, FastAPI app, all API endpoints, Gemini integrations |
| **Yashi** | Mac M3 Pro | Module service logic: Scam Sentinel processing, Fraud Graph engine, Geo Intel, Note Verify backend, Citizen Shield NLU |
| **Nivedita** | Mac M4 Air | Web dashboard (Next.js), Citizen mobile app (React Native/Expo), all UI screens |

---

## Repository Structure (MVP — Simplified)

```
primer/
├── backend/                    (Single FastAPI application)
│   ├── app/
│   │   ├── main.py             FastAPI app entry point
│   │   ├── config.py           Settings + env vars
│   │   ├── auth/               Login, JWT, middleware
│   │   ├── routers/
│   │   │   ├── scam_sentinel.py
│   │   │   ├── note_verify.py
│   │   │   ├── fraud_graph.py
│   │   │   ├── geo_intel.py
│   │   │   ├── citizen_shield.py
│   │   │   ├── copilot.py
│   │   │   ├── qr_scanner.py
│   │   │   ├── case_summary.py
│   │   │   ├── panic.py
│   │   │   └── call_screen.py
│   │   ├── models/             SQLAlchemy models
│   │   ├── services/           Business logic per module
│   │   ├── ml/                 Model loading + inference
│   │   └── utils/              Shared utilities
│   ├── migrations/             Alembic migration files
│   ├── seed_data/              Demo data SQL files
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│
├── frontend/
│   └── dashboard/              (Next.js web dashboard)
│       ├── src/
│       │   ├── app/            Pages (App Router)
│       │   ├── components/     UI components
│       │   └── styles/         CSS tokens + modules
│       ├── package.json
│       └── Dockerfile
│
├── mobile/                     (React Native / Expo citizen app)
│   ├── App.tsx
│   ├── screens/
│   ├── components/
│   └── package.json
│
├── ml/                         (Training scripts — Sumanth only)
│   ├── note-auth-net/          Currency model training
│   ├── voice-spoof-detector/   Voice deepfake training
│   ├── scam-classifier/        XGBoost scam classifier
│   └── hotspot-predictor/      Crime prediction model
│
├── docker-compose.yml          One command to run everything
├── .env.example                Environment variables template
└── README.md
```

---

## Execution Plan — 4 Phases

This plan is structured into 4 sequential phases, where each phase represents a single person's primary contribution.

### Phase 1 — Sumanth (Infrastructure & Machine Learning)

**Goal:** Establish the foundation (database, containers, seed data) and train all ML models.

```
PHASE 1: SUMANTH
─────────────────────────────────────────────────────────────
├── 1. Infrastructure
│   ├── [ ] Docker Compose: PostgreSQL + PostGIS + pgvector + Redis
│   ├── [ ] Database migrations (all schemas from Backend Schema doc)
│   ├── [ ] Seed data: 50+ scam sessions, 100+ graph entities, 200+ geo incidents
│   └── [ ] Verify: docker compose up → all healthy
│
├── 2. ML Models Training
│   ├── [ ] NoteAuthNet training (EfficientNet-B4) → model.pth & model.tflite
│   ├── [ ] VoiceSpoofDetector training (LCNN) → voice_spoof.pth
│   ├── [ ] XGBoost scam classifier → scam_classifier.joblib
│   └── [ ] Hotspot Predictor (Random Forest) → hotspot_predictor.joblib
│
├── 3. Agentic Orchestrator & Integration
│   ├── [ ] Export trained models to backend/app/ml/ and mobile/assets/
│   ├── [ ] Test inference scripts
│   ├── [ ] Adaptive KB: embedding pipeline for new scam patterns
│   └── [ ] Gemini API integration helpers (function calling schemas)
```

### Phase 2 — Yashi (Module Services & Business Logic)

**Goal:** Implement the core business logic, algorithms, and prompt engineering that power the modules.

```
PHASE 2: YASHI
─────────────────────────────────────────────────────────────
├── 1. Scam Sentinel & Graph Logic
│   ├── [ ] Signal score computation logic & script similarity matching (FAISS)
│   ├── [ ] Alert level classification (RED/AMBER/YELLOW)
│   ├── [ ] Fraud Graph: 2-hop neighbourhood query (recursive CTE)
│   ├── [ ] Fraud Graph: Community detection & money flow tracing
│   └── [ ] Graph data → JSON format for frontend visualisation
│
├── 2. Geo Intel & Citizen Shield Logic
│   ├── [ ] PostGIS heatmap aggregation & incident pins queries
│   ├── [ ] Hotspot prediction integration
│   ├── [ ] Citizen Shield: Gemini prompt engineering & language detection
│   └── [ ] Knowledge Base: similarity search + labeling flow
│
├── 3. Extra Features Logic
│   ├── [ ] AI Copilot: query parsing → SQL generation → result formatting
│   ├── [ ] QR Scanner: UPI parsing, URL domain reputation check
│   ├── [ ] Case Summarizer: evidence extraction pipeline
│   ├── [ ] Deepfake voice: inference wrapper for VoiceSpoofDetector
│   └── [ ] Dossier PDF template (Jinja2 + WeasyPrint)
```

### Phase 3 — Srinivas (Core Backend APIs)

**Goal:** Wrap the logic in a robust FastAPI application, handle authentication, and expose all necessary endpoints.

```
PHASE 3: SRINIVAS
─────────────────────────────────────────────────────────────
├── 1. FastAPI Setup & Auth
│   ├── [ ] Project scaffold: FastAPI + SQLAlchemy + Alembic
│   ├── [ ] Auth router: login → JWT → middleware
│   ├── [ ] Seed demo users: Yashi, Srinivas, Sumanth
│   └── [ ] Health check + CORS + error handling
│
├── 2. Core Module APIs
│   ├── [ ] Scam Sentinel: GET /scam/sessions, GET /scam/stats, POST /scam/acknowledge
│   ├── [ ] Scam Sentinel: WebSocket /ws/scam/live (real-time feed)
│   ├── [ ] Note Verify: POST /note/verify, GET /note/history, GET /note/stats
│   ├── [ ] Fraud Graph: GET /graph/entity/{id}, POST /graph/dossier
│   └── [ ] Geo Intel: GET /geo/heatmap, GET /geo/predictions
│
├── 3. Extra Feature APIs & Polish
│   ├── [ ] Citizen Shield: POST /citizen/chat, GET /citizen/number-check
│   ├── [ ] Extra Features: POST /copilot/query, POST /qr/scan, POST /case/summarize
│   ├── [ ] Extra Features: POST /panic/trigger, GET /screen/number/{phone}
│   └── [ ] API Testing: ensure all endpoints handle errors gracefully
```

### Phase 4 — Nivedita (Frontend & Mobile Apps)

**Goal:** Build the user interfaces, connect them to the backend, and prepare for the final demo.

```
PHASE 4: NIVEDITA
─────────────────────────────────────────────────────────────
├── 1. Web Dashboard Shell & Core UI
│   ├── [ ] Next.js project setup + design tokens (globals.css)
│   ├── [ ] Navbar, Sidebar, Layout, Login page
│   ├── [ ] Home Dashboard: stat cards, threat level bar, live alert feed
│   ├── [ ] Scam Sentinel: Live Monitor screen + Session detail drawer
│   └── [ ] Fraud Graph Explorer (Sigma.js) + Geo Intel Crime Map (Mapbox)
│
├── 2. Mobile App Setup
│   ├── [ ] Expo project setup + Home screen feature grid
│   ├── [ ] Note scanner screen (camera integration)
│   ├── [ ] QR Scanner screen (camera → decode → risk verdict)
│   ├── [ ] AI Chat screen & Number Check screen
│   └── [ ] Call Screening overlay & Panic Button screen
│
├── 3. Integration & Demo Polish
│   ├── [ ] Connect all screens to live APIs (Srinivas's endpoints)
│   ├── [ ] Ensure animations (RED card pulse, count-ups) are smooth (60fps)
│   ├── [ ] End-to-end testing (Login → Dashboard → Graph → Map)
│   └── [ ] Rehearse 5-minute demo script & verify seed data
```

---

## Dependency Graph

```
Sumanth (Infra)  ──→  Srinivas (Backend)  ──→  Nivedita (Frontend)
     │                      ↑                       ↑
     │                      │                       │
     └── ML Models ─────────┘                       │
                             │                       │
Yashi (Module Logic) ────────┘───────────────────────┘
```

- **Sumanth** unblocks everyone: Docker + DB + models
- **Srinivas** unblocks Nivedita: APIs must exist before UI can connect
- **Yashi** works in parallel with Srinivas: implements business logic that APIs call
- **Nivedita** can start the shell immediately (no API needed for layout), then wires up

---

## Demo Day Checklist

```
Pre-Demo (30 min before):
[ ] docker compose up -d → all services healthy
[ ] Run seed script → fresh demo data
[ ] Dashboard loads at localhost:3000
[ ] Mobile app running on physical phone
[ ] Test: login as each of 3 demo users
[ ] Test: Scam Sentinel live feed shows sessions
[ ] Test: Graph Explorer renders a cluster
[ ] Test: Map shows heatmap
[ ] Test: QR Scanner works on physical QR code
[ ] Test: AI Copilot answers a query

During Demo:
[ ] Follow 5-minute script from Application Flow doc §14
[ ] Start with Dashboard (impressive first impression)
[ ] Show Explainable AI (judges love transparency)
[ ] Show AI Copilot (judges love natural language)
[ ] Switch to mobile for citizen features
[ ] End with Panic Button (emotional impact)
```
