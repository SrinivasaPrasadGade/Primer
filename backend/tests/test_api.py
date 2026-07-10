"""API-layer tests for Srinivas's routers — auth, role-based access, error handling,
and happy-path response shaping. The DB session and Yashi/Sumanth service functions are
faked/monkeypatched so these run without a live Postgres, FAISS index, or model files.
"""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.main import app

DEMO_USER_ID = "11111111-1111-1111-1111-111111111111"


# ---------------------------------------------------------------------------
# Fakes + fixtures
# ---------------------------------------------------------------------------

class FakeResult:
    """Mimics SQLAlchemy's Result: .mappings().first() / .all()."""

    def __init__(self, first=None, rows=None):
        self._first = first
        self._rows = rows or []

    def mappings(self):
        return self

    def first(self):
        return self._first

    def all(self):
        return self._rows


class FakeSession:
    """Async DB stand-in. Tests queue results; execute() pops them in order."""

    def __init__(self):
        self._queue: list[FakeResult] = []
        self.default = FakeResult()

    def queue(self, *results: FakeResult) -> "FakeSession":
        self._queue.extend(results)
        return self

    async def execute(self, *args, **kwargs):
        return self._queue.pop(0) if self._queue else self.default

    async def commit(self):
        pass


@pytest.fixture
def db():
    return FakeSession()


@pytest.fixture
def client(db):
    async def _get_db():
        yield db

    app.dependency_overrides[get_db] = _get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def login_as(role: str):
    """Override the auth dependency to simulate a bearer token for `role`."""

    async def _current_user():
        return {
            "id": DEMO_USER_ID,
            "email": "demo@primer.demo",
            "name": "Demo",
            "role": role,
            "designation": None,
            "jurisdiction": "Mumbai Suburban",
            "is_active": True,
        }

    app.dependency_overrides[get_current_user] = _current_user


# ---------------------------------------------------------------------------
# Health + auth
# ---------------------------------------------------------------------------

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_protected_route_requires_token(client):
    # No get_current_user override => HTTPBearer finds no credentials => 401.
    r = client.get("/api/v1/scam/stats")
    assert r.status_code == 401


def test_login_invalid_credentials(client, db):
    db.queue(FakeResult(first=None))  # no user with that email
    r = client.post("/api/v1/auth/login", json={"email": "nobody@primer.demo", "password": "x"})
    assert r.status_code == 401


def test_login_success(client, db, monkeypatch):
    monkeypatch.setattr("app.auth.router.verify_password", lambda plain, hashed: True)
    db.queue(
        FakeResult(
            first={
                "id": uuid4(),
                "email": "srinivas@primer.demo",
                "name": "Srinivas",
                "role": "bank_manager",
                "designation": "Branch Manager, SBI",
                "jurisdiction": "Andheri West",
                "password_hash": "$2b$12$whatever",
                "is_active": True,
            }
        )
    )
    r = client.post("/api/v1/auth/login", json={"email": "srinivas@primer.demo", "password": "Primer@2026"})
    assert r.status_code == 200
    body = r.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["user"]["role"] == "bank_manager"


def test_me_returns_current_user(client):
    login_as("citizen")
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 200
    assert r.json()["role"] == "citizen"


# ---------------------------------------------------------------------------
# Role-based access control
# ---------------------------------------------------------------------------

def test_scam_sessions_forbidden_for_citizen(client):
    login_as("citizen")
    r = client.get("/api/v1/scam/sessions")
    assert r.status_code == 403


def test_scam_sessions_allowed_for_officer(client, db):
    login_as("lea_officer")
    db.queue(FakeResult(rows=[]))
    r = client.get("/api/v1/scam/sessions")
    assert r.status_code == 200
    assert r.json() == []


def test_communities_detect_requires_lea_officer(client):
    login_as("bank_manager")  # only lea_officer may run detection
    r = client.post("/api/v1/graph/communities/detect")
    assert r.status_code == 403


# ---------------------------------------------------------------------------
# Not-found + error handling
# ---------------------------------------------------------------------------

def test_scam_session_detail_not_found(client, monkeypatch):
    login_as("lea_officer")
    monkeypatch.setattr("app.services.scam_sentinel.get_session_detail", _async_return(None))
    r = client.get(f"/api/v1/scam/sessions/{uuid4()}")
    assert r.status_code == 404


def test_classify_missing_session_maps_to_404(client, monkeypatch):
    login_as("lea_officer")

    async def _raise(*args, **kwargs):
        raise ValueError("Scam session not found")

    monkeypatch.setattr("app.services.scam_sentinel.process_scam_session", _raise)
    r = client.post(f"/api/v1/scam/sessions/{uuid4()}/classify")
    assert r.status_code == 404


def test_note_verify_rejects_empty_image(client):
    login_as("citizen")
    r = client.post(
        "/api/v1/note/verify",
        data={"denomination": "500"},
        files={"image": ("note.jpg", b"", "image/jpeg")},
    )
    assert r.status_code == 400


def test_number_check_public_no_auth(client, monkeypatch):
    # number-check is intentionally public (no login_as()).
    monkeypatch.setattr("app.services.scam_sentinel.get_number_reputation", _async_return(None))
    r = client.get("/api/v1/citizen/number-check/+919999999999")
    assert r.status_code == 200
    assert r.json()["risk_score"] == 0


# ---------------------------------------------------------------------------
# Happy-path delegation
# ---------------------------------------------------------------------------

def test_qr_scan_delegates_to_service(client, monkeypatch):
    login_as("citizen")
    monkeypatch.setattr(
        "app.services.qr_scanner.scan_qr_code",
        _async_return({"id": "abc", "risk_level": "safe", "content_type": "url"}),
    )
    r = client.post("/api/v1/qr/scan", json={"qr_content": "https://example.com"})
    assert r.status_code == 200
    assert r.json()["risk_level"] == "safe"


def test_screen_number_low_risk_default(client, monkeypatch):
    login_as("citizen")
    monkeypatch.setattr("app.services.scam_sentinel.get_number_reputation", _async_return(None))
    r = client.get("/api/v1/screen/number/+919812345678")
    assert r.status_code == 200
    body = r.json()
    assert body["risk_level"] == "low"
    assert body["recommendation"] == "allow"


def test_screen_number_high_risk_blocks(client, monkeypatch):
    login_as("lea_officer")
    monkeypatch.setattr(
        "app.services.scam_sentinel.get_number_reputation",
        _async_return({"risk_score": 90, "is_blacklisted": True, "primary_scam_type": "digital_arrest"}),
    )
    r = client.get("/api/v1/screen/number/+919800000000")
    assert r.status_code == 200
    body = r.json()
    assert body["risk_level"] == "high"
    assert body["recommendation"] == "block"
    assert "blacklisted" in body["flags"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _async_return(value):
    async def _fn(*args, **kwargs):
        return value

    return _fn
