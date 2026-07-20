# Primer

**AI-powered digital public safety intelligence platform.** An officer-facing web
dashboard and a citizen-facing mobile app over a FastAPI backend, covering scam-call
detection, counterfeit-note verification, fraud-network analysis, geospatial crime
intelligence, and citizen self-service.

---

## Architecture

```
                 ┌──────────────────────┐      ┌──────────────────────┐
                 │  Web Dashboard       │      │  Mobile App          │
                 │  Next.js 15 (:3000)  │      │  Expo / RN           │
                 │  officers, analysts  │      │  citizens            │
                 └──────────┬───────────┘      └──────────┬───────────┘
                            │  REST + WebSocket           │  REST
                            └──────────────┬──────────────┘
                                           ▼
                        ┌─────────────────────────────────────┐
                        │  FastAPI  (:8000)  /api/v1          │
                        │  routers → services → SQL           │
                        │  JWT auth, role-gated (lea_officer, │
                        │  bank_manager, citizen)             │
                        └───┬───────────────┬─────────────┬───┘
                            │               │             │
              ┌─────────────▼──┐   ┌────────▼──────┐   ┌──▼──────────────┐
              │ PostgreSQL 16  │   │ Redis 7       │   │ ML artifacts    │
              │ + PostGIS      │   │ live-feed     │   │ app/ml/models/  │
              │ + pgvector     │   │ pub/sub       │   │ .joblib .pth    │
              │ 9 schemas      │   │               │   │ .faiss          │
              └────────────────┘   └───────────────┘   └─────────────────┘
```

**Modules.** Scam Sentinel (5-signal call scoring + live feed) · Note Verify
(counterfeit detection) · Fraud Graph (entity network, community detection,
dossiers) · Geo Intel (PostGIS heatmap + hotspot prediction) · Citizen Shield (AI
advisor, number checks) · QR Scanner · Case Summarizer · AI Copilot · Adaptive Fraud
KB · Panic Button · Pre-Answer Call Screening.

`routers/` handle HTTP, auth, and validation; `services/` hold the logic and own all
SQL. Routers never compute scores themselves.

---

## Quick start (Docker)

```bash
cp .env.example .env
# JWT_SECRET_KEY is REQUIRED — compose refuses to start without it:
#   openssl rand -hex 32
docker compose up -d
```

Then load the demo data (migrations create the schema and the three demo users;
`01_seed.sql` fills in the demo content):

```bash
docker exec -i primer-db psql -U primer -d primer < backend/seed_data/01_seed.sql
docker exec primer-api python -m scripts.bootstrap_predictions
```

| Service | URL |
| --- | --- |
| API + interactive docs | http://localhost:8000/docs |
| Web dashboard | http://localhost:3000 |

> `bootstrap_predictions` must run **after** `01_seed.sql` — the hotspot model scores
> each grid point from nearby incidents, so on an unseeded database nothing clears the
> threshold and the Geo Intel map shows 0 zones.

### Demo credentials

All three share the password **`Primer@2026`**.

| Email | Role | Sees |
| --- | --- | --- |
| `yashi@primer.demo` | `lea_officer` | everything — graph, geo, dossiers, live feed, SOS |
| `srinivas@primer.demo` | `bank_manager` | scam sessions, note verify, case summaries |
| `sumanth@primer.demo` | `citizen` | the mobile app (auto-signed-in) |

---

## ⚠️ Mobile: `localhost` will not work on a physical device

The mobile default API URL is `http://localhost:8000`. On a real phone `localhost`
is *the phone itself* — every request fails and the app hangs on its splash screen.

```bash
cd mobile
cp .env.example .env
# EXPO_PUBLIC_API_URL=http://192.168.1.42:8000   ← your machine's LAN IP
npx expo start
```

Find your IP with `ipconfig` (Windows) or `ifconfig | grep inet` (macOS/Linux); phone
and computer must share a network. `EXPO_PUBLIC_*` is inlined at build time, so
**restart the Expo dev server after editing `.env`** — a stale bundle keeps the old
URL and looks identical. See [`mobile/README.md`](mobile/README.md) for more.

---

## Local development (without Docker)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt

alembic upgrade head
psql "$DATABASE_URL" -f seed_data/00_extensions.sql -f seed_data/01_seed.sql
python -m scripts.bootstrap_predictions

uvicorn app.main:app --reload --reload-dir app --host 0.0.0.0 --port 8000
```

You still need Postgres and Redis — `docker compose up -d postgres redis` is the
easiest way.

> `requirements-dev.txt` must be installed for the tests to run at all. `pytest-asyncio`
> is pinned deliberately: an incompatible pair fails at *collection*, so every module
> errors out and nothing runs.

> `--reload-dir app` scopes the file watcher to source. Without it uvicorn also watches
> `.venv/`, and every installed package can trigger a spurious full reload.

### Tests

```bash
cd backend && .venv/bin/pytest        # Windows: .venv\Scripts\pytest
```

### Dashboard

```bash
cd frontend/dashboard
npm install
npm run dev                           # http://localhost:3000
```

---

## Demo helpers

**Make the live feed move.** Nothing creates scam sessions on its own, so
**Scam Sentinel → Live Monitor** sits still. With the API up, in a second terminal:

```bash
cd backend
python -m scripts.simulate_live_feed --interval 3
```

It inserts a call record and classifies it on a timer, so the board reacts during a
pitch. It classifies over HTTP on purpose — the live-feed broadcast happens in the API
process, so a script calling the service directly would score sessions silently.

**Populate the fraud KB.** The seeded patterns ship without embeddings, so similarity
search returns nothing until they're generated once:

```bash
curl -X POST http://localhost:8000/api/v1/kb/backfill-embeddings \
  -H "Authorization: Bearer $TOKEN"
```

---

## Troubleshooting

| Symptom | Cause |
| --- | --- |
| `docker compose up` errors on `JWT_SECRET_KEY` | Working as intended — set it in `.env`. The default in `config.py` is public. |
| API serves only `/health` | Stale image. `docker compose build backend` and watch for a pip failure — a failed build silently leaves the old image running. |
| Login returns 401 for every demo user | Database predates the committed password hashes. Migration `0002` repairs it; on a very old volume, `docker compose down -v` and re-seed. |
| Geo Intel map shows 0 predicted zones | `bootstrap_predictions` hasn't run, or ran before `01_seed.sql`. |
| Live Monitor never updates | Nothing generates sessions — run `simulate_live_feed`. |
| Mobile app stuck on splash | `EXPO_PUBLIC_API_URL` still `localhost` on a physical device, or the backend isn't running. |
| `/api/v1/kb/match` returns no matches | Run `backfill-embeddings` once. |

---

## Repo layout

```
backend/          FastAPI app, Alembic migrations, ML artifacts, demo scripts
  app/routers/    HTTP layer — auth, validation, response shaping
  app/services/   logic layer — all SQL and model inference
  app/ml/models/  trained artifacts (.joblib, .pth, .faiss)
  scripts/        bootstrap_predictions, simulate_live_feed
frontend/dashboard/  Next.js officer dashboard
mobile/           Expo citizen app
postgres/         PostGIS + pgvector image
```

Design and planning docs live at the repo root: `product_requirements_document.md`,
`technical_requirements_document.md`, `backend_api_contract.md`,
`backend_schema_document.md`, `ui_ux_design_document.md`,
`application_flow_document.md`, plus the per-person task sheets.
