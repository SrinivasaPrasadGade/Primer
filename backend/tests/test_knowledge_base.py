"""Unit tests for app.services.knowledge_base — mocked embedder + AsyncSession, no live Postgres needed."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.services import knowledge_base as svc


class FakeResult:
    def __init__(self, row=None, rows=None):
        self._row = row
        self._rows = rows or []

    def mappings(self):
        return self

    def first(self):
        return self._row

    def all(self):
        return self._rows


@pytest.fixture(autouse=True)
def fake_embedder(monkeypatch):
    class FakeEmbedder:
        def encode(self, texts, normalize_embeddings=True):
            import numpy as np

            return np.zeros((1, 384), dtype="float32")

    monkeypatch.setattr(svc, "_load_embedder", lambda: FakeEmbedder())


@pytest.mark.asyncio
async def test_find_similar_patterns():
    rows = [
        {"id": uuid4(), "title": "Customs Seizure", "description": "d", "scam_type": "customs_seizure",
         "key_indicators": ["fir", "penalty"], "similarity": 0.91},
    ]
    db = AsyncMock()
    db.execute.return_value = FakeResult(rows=rows)

    result = await svc.find_similar_patterns(db, "a customs officer is threatening me", top_k=5)

    assert len(result) == 1
    assert result[0]["similarity"] == 0.91
    params = db.execute.call_args[0][1]
    assert params["top_k"] == 5
    assert params["embedding"].startswith("[") and params["embedding"].endswith("]")
    assert params["embedding"].count(",") == 383


@pytest.mark.asyncio
async def test_find_similar_patterns_empty():
    db = AsyncMock()
    db.execute.return_value = FakeResult(rows=[])
    result = await svc.find_similar_patterns(db, "some description")
    assert result == []


@pytest.mark.asyncio
async def test_add_pattern():
    pattern_id = uuid4()
    labeled_by = uuid4()
    db = AsyncMock()
    db.execute.return_value = FakeResult(
        row={
            "id": pattern_id, "title": "New Scam", "description": "desc", "scam_type": "phishing",
            "language": "en", "key_indicators": ["urgent"], "verified": False,
            "labeled_by": labeled_by, "created_at": None,
        }
    )

    result = await svc.add_pattern(db, "New Scam", "desc", "phishing", labeled_by, key_indicators=["urgent"])

    assert result["id"] == str(pattern_id)
    assert result["verified"] is False
    db.commit.assert_awaited_once()
    params = db.execute.call_args[0][1]
    assert isinstance(params["embedding"], str) and params["embedding"].startswith("[")
    assert params["key_indicators"] == ["urgent"]


@pytest.mark.asyncio
async def test_add_pattern_defaults_key_indicators():
    db = AsyncMock()
    db.execute.return_value = FakeResult(row={"id": uuid4(), "title": "t", "description": "d",
                                               "scam_type": "phishing", "language": "en",
                                               "key_indicators": [], "verified": False,
                                               "labeled_by": uuid4(), "created_at": None})
    await svc.add_pattern(db, "t", "d", "phishing", uuid4())
    params = db.execute.call_args[0][1]
    assert params["key_indicators"] == []


@pytest.mark.asyncio
async def test_verify_pattern_found():
    pattern_id = uuid4()
    db = AsyncMock()
    db.execute.return_value = FakeResult(row={"id": pattern_id, "title": "t", "scam_type": "phishing", "verified": True})
    result = await svc.verify_pattern(db, pattern_id)
    assert result["verified"] is True
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_verify_pattern_not_found():
    db = AsyncMock()
    db.execute.return_value = FakeResult(row=None)
    result = await svc.verify_pattern(db, uuid4())
    assert result is None
