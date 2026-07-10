# Backend API Contract — Frontend/Mobile Integration Handoff

> **From:** Srinivas (Phase 3 — core backend) → **To:** Nivedita (Phase 4 — frontend/mobile)
> This is the single source of truth for wiring up screens. Every route below is
> live on the running backend. Interactive docs: **http://localhost:8000/docs**.

---

## 1. Getting the backend running

```bash
docker compose up -d postgres redis
cd backend
source .venv/bin/activate            # or your venv
alembic upgrade head                  # creates schema + seeds the 3 demo users
psql "$DATABASE_URL" -f seed_data/00_extensions.sql -f seed_data/01_seed.sql
uvicorn app.main:app --reload --reload-dir app --host 0.0.0.0 --port 8000
```

> `--reload-dir app` scopes the file-watcher to just the `app/` source directory.
> Without it, uvicorn also watches your `.venv/`, so every import in every installed
> package (torch, sklearn, sqlalchemy, ...) can trigger a spurious full reload —
> harmless, but it buries your actual request logs in noise.

- **Base URL:** `http://localhost:8000`
- **All endpoints below are under `/api/v1`** (matches your `lib/api.ts` `API_BASE + "/api/v1"`).
- **CORS** is already open for `http://localhost:3000` (Next.js) and `http://localhost:19006` (Expo). If you run the dashboard on a different port, tell me and I'll add it.

---

## 2. Auth

JWT bearer tokens, 24h expiry, no refresh (MVP). Send `Authorization: Bearer <token>`
on every call except the two explicitly marked **public** below.

### Demo credentials (all password `Primer@2026`)

| Email | Role | Use for |
|---|---|---|
| `yashi@primer.demo` | `lea_officer` | Dashboard, Scam, Graph, Geo, Copilot, Case |
| `srinivas@primer.demo` | `bank_manager` | Note Verify dashboard |
| `sumanth@primer.demo` | `citizen` | Mobile app flows |

### `POST /api/v1/auth/login`
```jsonc
// request
{ "email": "yashi@primer.demo", "password": "Primer@2026" }
// response
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": { "id": "...", "email": "...", "name": "Yashi",
            "role": "lea_officer", "designation": "...", "jurisdiction": "..." }
}
```

### `GET /api/v1/auth/me` → the current user object (same shape as `user` above)

**Auth failures:** `401` (no/expired/invalid token), `403` (valid token, wrong role).

---

## 3. Endpoints by module

Role column: **any** = any logged-in user; **public** = no token needed.

### Scam Sentinel — `/scam`
| Method | Path | Role | Notes |
|---|---|---|---|
| GET | `/scam/sessions?alert_level=&status=&limit=&offset=` | lea_officer, bank_manager | list, newest first |
| GET | `/scam/sessions/{id}` | lea_officer, bank_manager | detail + `signal_scores` for Explainable AI |
| POST | `/scam/sessions/{id}/classify` | lea_officer, bank_manager | (re)runs scoring, broadcasts to WS |
| POST | `/scam/sessions/{id}/acknowledge` | lea_officer, bank_manager | officer ack |
| GET | `/scam/numbers/{phone}` | any | number reputation |
| POST | `/scam/numbers/{phone}/flag` | lea_officer, bank_manager | body `{ "alert_level": "RED" }` |
| GET | `/scam/stats` | any | dashboard tiles |
| **WS** | `/api/v1/scam/ws/live` | — | live session feed (see §4) |

`signal_scores` shape (feeds your `ExplainableAI` component):
```jsonc
{ "call_flow_match":  { "score": 0.91, "explanation": "..." },
  "number_spoofing":  { "score": 0.80, "explanation": "..." },
  "script_similarity":{ "score": 0.71, "explanation": "..." },
  "voice_synthetic":  { "score": 0.67, "explanation": "..." },
  "urgency_phrases":  { "score": 0.89, "explanation": "..." } }
```

### Note Verify — `/note`
| Method | Path | Role | Notes |
|---|---|---|---|
| POST | `/note/verify` | any | **JSON base64** (see below) |
| GET | `/note/history?limit=` | any | current user's scans |
| GET | `/note/stats` | any | FICN analytics |
| GET | `/note/serials/{serial}` | any | 404 if not a known counterfeit |

```jsonc
// POST /note/verify  — matches your api.ts verifyNote()
{ "image_base64": "<base64 or data:image/jpeg;base64,...>",
  "denomination": 500,          // optional, defaults 500
  "serial_number": "9AB123456", // optional
  "scan_source": "mobile",      // "mobile" | "web" | "scanner"
  "lat": 19.07, "lng": 72.87 }  // optional
// response: { verdict: "GENUINE"|"SUSPECT"|"COUNTERFEIT", confidence, feature_analysis, ... }
```

### Fraud Graph — `/graph`
| Method | Path | Role | Notes |
|---|---|---|---|
| GET | `/graph/entity/{type}/{value}?depth=2` | any | `{ nodes, edges }` for Sigma.js |
| GET | `/graph/cluster/{id}` | any | `{ cluster, entities, edges }` |
| GET | `/graph/money-flow/{entity_id}` | any | transfer chain |
| POST | `/graph/search` | any | body `{ "query": "9198...", "limit": 20 }` |
| POST | `/graph/dossier/{cluster_id}` | lea_officer, bank_manager | generates PDF, returns `{ pdf_path }` |
| POST | `/graph/communities/detect?min_cluster_size=3` | lea_officer | re-runs clustering |

`type` ∈ `phone_number, bank_account, upi_id, person, device, ip_address, complaint`.

### Geo Intel — `/geo`
| Method | Path | Role | Notes |
|---|---|---|---|
| GET | `/geo/heatmap?bounds=&type=&days=` | any | grid-aggregated intensities |
| GET | `/geo/incidents?bounds=&type=&limit=` | any | individual pins |
| GET | `/geo/predictions?bounds=&prediction_date=` | any | stored hotspot zones |
| POST | `/geo/predictions/generate?bounds=&type=&grid_km=&risk_threshold=` | lea_officer | compute + store |
| GET | `/geo/stats` | any | by crime_type/state/district |

**`bounds` = `"west,south,east,north"`** (one comma-separated string, matches your
Mapbox `map.getBounds()`). Example: `?bounds=72.77,18.89,72.99,19.27`.
Mumbai suburban is a good default viewport. `type` is optional crime-type filter.

### Citizen Shield — `/citizen`
| Method | Path | Role | Notes |
|---|---|---|---|
| POST | `/citizen/chat` | any | body `{ "message": "...", "session_id": null }` — omit `session_id` to start; response includes `session_id` + `reply` |
| GET | `/citizen/chat/{session_id}/history` | any | full transcript |
| POST | `/citizen/chat/{session_id}/close` | any | end session |
| GET | `/citizen/number-check/{phone}` | **public** | citizen number lookup |

### Extra features
| Method | Path | Role | Body / Notes |
|---|---|---|---|
| POST | `/copilot/query` | any | `{ "question": "..." }` → `{ answer, data, sources, query_executed }` |
| POST | `/qr/scan` | any | `{ "qr_content": "upi://..." }` → risk verdict |
| POST | `/case/summarize` | lea_officer, bank_manager | `{ "entity_type": "...", "entity_value": "...", "investigation_id": null }` |
| POST | `/panic/trigger` | any | `{ caller_number?, call_duration_sec?, location?{lat,lng}, emergency_contact_number? }` |
| GET | `/screen/number/{phone}` | any | `{ risk_level, risk_score, flags, recommendation }` |

---

## 4. WebSocket — live scam feed

```ts
// your useWebSocket hook — full URL:
const { messages } = useWebSocket("ws://localhost:8000/api/v1/scam/ws/live");
```
The socket pushes a JSON object each time a session is classified (via
`POST /scam/sessions/{id}/classify`), shape:
`{ session_id, alert_level, overall_confidence, signal_scores }`.
Send any text periodically (or nothing) — the server only uses it as keep-alive.
The hook you sketched already auto-reconnects; no auth handshake needed for the demo.

---

## 5. Known gotchas / conventions

- **Decimals come back as JSON numbers**, not strings (e.g. `overall_confidence: 74.3`) — safe to `.toFixed()`.
- **404 vs empty:** list endpoints return `[]` when empty; single-resource GETs return `404`. `number-check` and `screen/number` return a low-risk object rather than 404 for unknown numbers.
- **Errors** are always `{ "detail": "message" }`. Show `detail` in your error toasts.
- Two endpoints differ slightly from the illustrative examples in the older task sheets — **this doc is authoritative**: WS is `/api/v1/scam/ws/live`, and geo bounds is a single `bounds` string.

---

## 6. Integration checklist (Nivedita — tick as you wire each up)

- [ ] Login → store token → `api.setToken()`
- [ ] Dashboard stats from `/scam/stats`
- [ ] Scam live monitor: `/scam/sessions` + WS feed
- [ ] Session detail + Explainable AI from `/scam/sessions/{id}`
- [ ] Note Verify dashboard: `/note/verify` (base64) + `/note/stats`
- [ ] Fraud Graph: `/graph/entity/{type}/{value}`
- [ ] Geo map: `/geo/heatmap` + `/geo/incidents` (bounds string)
- [ ] Copilot chat: `/copilot/query`
- [ ] Mobile QR: `/qr/scan`; Panic: `/panic/trigger`; Chat: `/citizen/chat`

Ping me on any shape that doesn't match — happy to adjust the backend rather than
have you work around it.
