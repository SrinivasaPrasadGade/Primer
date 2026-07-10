# Srinivas — Core Backend (Mac M3 Air)

## **Primer — Developer Task Sheet**

| Field | Detail |
|---|---|
| **Owner** | Srinivas |
| **Machine** | MacBook Air M3, 8GB RAM |
| **Role** | Core backend: FastAPI app, Auth, all API endpoints, Gemini integration |
| **Stack** | Python 3.12, FastAPI, SQLAlchemy 2.0, asyncpg, Redis, Gemini API |
| **Companion Docs** | [TRD](technical_requirements_document.md) · [Backend Schema](backend_schema_document.md) |

---

## 1. Machine Setup

### 1.1 Dev Tools

```bash
# Install Python 3.12 (if not already)
brew install python@3.12

# Install Docker Desktop (for local PostgreSQL + Redis)
# Download from https://www.docker.com/products/docker-desktop/
# IMPORTANT: Docker Desktop on M3 Air uses Rosetta. Limit memory to 4GB max.

# Install project tools
pip install uv  # Fast package manager
```

### 1.2 Project Init

```bash
cd primer/backend

# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

### 1.3 requirements.txt

```
# Core
fastapi==0.115.*
uvicorn[standard]==0.34.*
pydantic==2.*
pydantic-settings==2.*

# Database
sqlalchemy[asyncio]==2.*
asyncpg==0.30.*
alembic==1.15.*
pgvector==0.3.*

# Auth
python-jose[cryptography]==3.*
passlib[bcrypt]==1.*

# Redis
redis[hiredis]==5.*

# Gemini API
google-generativeai==0.7.1   # NOTE: the classic google.generativeai SDK, NOT the newer
                             # `google-genai` package. Sumanth already ships
                             # app/services/gemini_client.py against this one — don't swap it.

# ML inference (lightweight — heavy training is Sumanth's job)
joblib==1.*
numpy==2.*

# PDF generation
weasyprint==63.*
jinja2==3.*

# Utilities
python-multipart==0.0.*
httpx==0.28.*
python-dotenv==1.*
```

### 1.4 Environment Variables (.env)

```env
# Database
DATABASE_URL=postgresql+asyncpg://primer:primer_dev@localhost:5432/primer

# Redis
REDIS_URL=redis://localhost:6379

# Auth
JWT_SECRET_KEY=primer-hackathon-secret-change-me
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24

# Gemini API
GEMINI_API_KEY=your-gemini-api-key

# File storage
UPLOAD_DIR=./uploads
```

---

## 2. FastAPI Application Structure

### 2.1 Entry Point — `app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.auth.router import router as auth_router
from app.routers.scam_sentinel import router as scam_router
from app.routers.note_verify import router as note_router
from app.routers.fraud_graph import router as graph_router
from app.routers.geo_intel import router as geo_router
from app.routers.citizen_shield import router as citizen_router
from app.routers.copilot import router as copilot_router
from app.routers.qr_scanner import router as qr_router
from app.routers.case_summary import router as case_router
from app.routers.panic import router as panic_router
from app.routers.call_screen import router as screen_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to DB, load models, init Redis
    yield
    # Shutdown: close connections

app = FastAPI(
    title="Primer API",
    description="AI-Powered Digital Public Safety Intelligence Platform",
    version="1.0.0-mvp",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:19006"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(scam_router, prefix="/api/v1/scam", tags=["Scam Sentinel"])
app.include_router(note_router, prefix="/api/v1/note", tags=["Note Verify"])
app.include_router(graph_router, prefix="/api/v1/graph", tags=["Fraud Graph"])
app.include_router(geo_router, prefix="/api/v1/geo", tags=["Geo Intel"])
app.include_router(citizen_router, prefix="/api/v1/citizen", tags=["Citizen Shield"])
app.include_router(copilot_router, prefix="/api/v1/copilot", tags=["AI Copilot"])
app.include_router(qr_router, prefix="/api/v1/qr", tags=["QR Scanner"])
app.include_router(case_router, prefix="/api/v1/case", tags=["Case Summary"])
app.include_router(panic_router, prefix="/api/v1/panic", tags=["Panic Button"])
app.include_router(screen_router, prefix="/api/v1/screen", tags=["Call Screening"])

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0-mvp"}
```

### 2.2 Auth — `app/auth/`

```python
# app/auth/router.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.auth.jwt import create_access_token, get_current_user

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    user: dict

@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest, db=Depends(get_db)):
    user = await db.execute(
        select(User).where(User.email == req.email)
    )
    user = user.scalar_one_or_none()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({
        "sub": str(user.id),
        "name": user.name,
        "role": user.role,
        "jurisdiction": user.jurisdiction,
    })
    return {"access_token": token, "user": user.to_dict()}

@router.get("/me")
async def me(user=Depends(get_current_user)):
    return user
```

```python
# app/auth/jwt.py
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config import settings

def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRE_HOURS)
    return jwt.encode({**data, "exp": expire}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
```

---

## 3. API Endpoint Reference

### 3.1 What Srinivas Implements (All Routes)

| Router File | Prefix | Key Endpoints | Dependencies |
|---|---|---|---|
| `auth/router.py` | `/auth` | login, me | — |
| `scam_sentinel.py` | `/scam` | sessions CRUD, number lookup, stats, WebSocket live | Yashi: signal score logic |
| `note_verify.py` | `/note` | verify (image upload), history, stats | Sumanth: NoteAuthNet model |
| `fraud_graph.py` | `/graph` | entity lookup, cluster, search, money-flow, dossier | Yashi: graph query logic |
| `geo_intel.py` | `/geo` | incidents, heatmap, predictions, stats | Yashi: PostGIS queries, Sumanth: prediction model |
| `citizen_shield.py` | `/citizen` | chat, number-check | Yashi: prompt templates |
| `copilot.py` | `/copilot` | query | Yashi: query parsing logic |
| `qr_scanner.py` | `/qr` | scan | Yashi: risk assessment logic |
| `case_summary.py` | `/case` | summarize | Yashi: evidence extraction |
| `panic.py` | `/panic` | trigger | — (self-contained) |
| `call_screen.py` | `/screen` | number/{phone} | Uses number_reputation table |

### 3.2 Srinivas is the "API Layer" — Not the Logic Layer

**Rule:** Srinivas writes the HTTP handlers (request validation, response formatting, auth checks). Yashi writes the business logic (signal scoring, graph queries, PostGIS operations). Srinivas calls Yashi's service functions.

```python
# Srinivas writes this (router):
@router.get("/sessions/{session_id}")
async def get_session(session_id: UUID, db=Depends(get_db), user=Depends(require_role("lea_officer"))):
    session = await scam_service.get_session_with_signals(db, session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    return session

# Yashi writes this (service):
# app/services/scam_sentinel.py
async def get_session_with_signals(db, session_id: UUID):
    # Complex query joining session + computing signal explanations
    ...
```

---

## 4. Gemini API Integration

### 4.1 Setup

> **Already implemented by Sumanth** in `app/services/gemini_client.py` (Phase 1) — do
> not rewrite it. It uses the classic `google.generativeai` SDK (`google-generativeai==0.7.1`),
> lazy-configures from `settings.gemini_api_key`, and retries on rate limits. Import and
> call its async helpers rather than newing up a client. Available functions:
>
> | Function | Use |
> |---|---|
> | `generate(prompt, *, system_instruction=None, temperature=0.3, model_name=...)` | Plain text |
> | `generate_json(prompt, ...)` | JSON output, parsed (case summaries) |
> | `generate_with_tools(prompt, tools, ...)` + `extract_function_calls(response)` | Raw function-calling |
> | `run_with_tools(prompt, tools, dispatch, ...)` | Full function-calling loop (Copilot) |

```python
# app/services/gemini_client.py (as shipped — excerpt)
import google.generativeai as genai   # classic SDK, NOT `from google import genai`
from app.config import settings

DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_TEMPERATURE = 0.3

async def generate(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = DEFAULT_TEMPERATURE,
    model_name: str = DEFAULT_MODEL,
) -> str:
    """Generate plain text from a prompt (lazy-configures the API key, retries on 429)."""
    model = _build_model(system_instruction, tools=None, model_name=model_name)
    generation_config = genai.types.GenerationConfig(temperature=temperature)
    response = await _call_with_retries(
        lambda: model.generate_content(prompt, generation_config=generation_config)
    )
    return response.text
```

### 4.2 Used In

| Feature | How Gemini Is Used |
|---|---|
| **AI Copilot** | Parse NL query → function calling → structured DB query → format results |
| **Case Summarizer** | Ingest evidence text → generate structured summary JSON |
| **Citizen Shield** | Chat with fraud-domain context → risk assessment + guidance |
| **Explainable AI** | Generate human-readable explanations from signal scores |

### 4.3 Copilot Query Flow (Gemini Function Calling)

> **Note:** `app/services/copilot.py` (the `COPILOT_TOOLS` schema + the
> function-calling loop via `run_with_tools`) and a thin `app/routers/copilot.py`
> already exist from Sumanth's Phase 1. Srinivas's job here is just to confirm the
> router is mounted and returns cleanly; the tool schema below is illustrative of
> what's already there.

```python
# app/services/copilot.py
COPILOT_TOOLS = [
    {
        "name": "search_complaints",
        "description": "Search fraud complaints by phone, account, or UPI",
        "parameters": {
            "type": "object",
            "properties": {
                "phone": {"type": "string"},
                "upi_id": {"type": "string"},
                "account": {"type": "string"},
            }
        }
    },
    {
        "name": "get_entity_connections",
        "description": "Get fraud graph connections for an entity",
        "parameters": {
            "type": "object",
            "properties": {
                "entity_type": {"type": "string", "enum": ["phone_number", "bank_account", "upi_id"]},
                "entity_value": {"type": "string"}
            },
            "required": ["entity_type", "entity_value"]
        }
    },
    # ... more tools
]

async def process_copilot_query(question: str, db):
    # 1. Send question + tools to Gemini
    # 2. Gemini returns function call(s) to execute
    # 3. Execute against database
    # 4. Return results to Gemini for formatting
    # 5. Return formatted answer to user
    ...
```

---

## 5. WebSocket — Live Scam Feed

```python
# app/routers/scam_sentinel.py
from fastapi import WebSocket, WebSocketDisconnect
import json

connected_clients: list[WebSocket] = []

@router.websocket("/ws/scam/live")
async def scam_live_feed(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep alive
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def broadcast_new_session(session_data: dict):
    """Called when a new scam session is detected"""
    for client in connected_clients:
        await client.send_json(session_data)
```

---

## 6. PDF Generation (Evidence Dossier)

```python
# app/services/dossier.py
from weasyprint import HTML
from jinja2 import Template

DOSSIER_TEMPLATE = """
<html>
<head><style>
  body { font-family: Inter, sans-serif; margin: 40px; }
  .header { border-bottom: 2px solid #333; padding-bottom: 16px; }
  .section { margin-top: 24px; }
  .entity-table { width: 100%; border-collapse: collapse; }
  .entity-table td, .entity-table th { padding: 8px; border: 1px solid #ddd; }
</style></head>
<body>
  <div class="header">
    <h1>Primer — Fraud Investigation Dossier</h1>
    <p>Cluster: {{ cluster.name }} | Generated: {{ timestamp }}</p>
  </div>
  <div class="section">
    <h2>Summary</h2>
    <p>{{ summary }}</p>
  </div>
  <!-- ... more sections -->
</body>
</html>
"""

async def generate_dossier_pdf(cluster_data, output_path):
    html = Template(DOSSIER_TEMPLATE).render(**cluster_data)
    HTML(string=html).write_pdf(output_path)
```

---

## 7. Running Locally

```bash
# Start infrastructure (Sumanth's docker-compose)
docker compose up -d postgres redis

# Run backend
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# API docs available at:
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

### Resource Awareness (M3 Air, 8GB)

```
Budget: ~5.5GB usable (macOS takes ~2.5GB)
├── Docker (Postgres + Redis):  ~800MB
├── Python + FastAPI:           ~300MB
├── Model loading (inference):  ~500MB
└── Available:                  ~3.9GB ✅ Comfortable
```

**Do NOT run ML training on this machine.** That's Sumanth's job (RTX 4060). Srinivas only loads pre-trained models for inference.

---

## 8. Task Checklist (Phase 3: Srinivas)

### 1. FastAPI Setup & Auth

- [x] Project scaffold: FastAPI + SQLAlchemy + Alembic
- [x] Auth router: login + JWT + middleware + role check
- [x] Seed demo users (Yashi, Srinivas, Sumanth)
- [x] Health check + CORS + error handling

### 2. Core Module APIs

- [x] Scam Sentinel: `GET /scam/sessions`, `GET /scam/stats`, `POST /scam/sessions/{id}/acknowledge`
- [x] Scam Sentinel: WebSocket live feed (`/ws/scam/live`)
- [x] Note Verify: `POST /note/verify` (image upload), `GET /note/history`, `GET /note/stats`
- [x] Fraud Graph: `GET /graph/entity/{id}`, `POST /graph/dossier`
- [x] Geo Intel: `GET /geo/heatmap`, `GET /geo/predictions`

### 3. Extra Feature APIs & Polish

- [x] Citizen Shield: `POST /citizen/chat`, `GET /citizen/number-check`
- [x] AI Copilot: `POST /copilot/query`
- [x] QR Scanner: `POST /qr/scan`
- [x] Case Summarizer: `POST /case/summarize`
- [x] Panic Button: `POST /panic/trigger`
- [x] Call Screening: `GET /screen/number/{phone}`
- [x] API Testing: ensure all endpoints handle errors gracefully
- [x] Integration readiness for Nivedita: API contract aligned to the frontend/TRD
      spec (`/note/verify` now base64 JSON; `/geo` endpoints take a single `bounds`
      string + `type`), CORS configured, handoff reference written to
      `backend_api_contract.md`. Live end-to-end integration testing happens once
      Nivedita's Phase 4 frontend exists.
