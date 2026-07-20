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
async def test_match_and_record_pattern_records_top_hit():
    pattern_id = uuid4()
    db = AsyncMock()
    db.execute.return_value = FakeResult(
        rows=[
            {"id": pattern_id, "title": "Digital Arrest", "description": "d",
             "scam_type": "digital_arrest", "key_indicators": [], "similarity": 0.88},
            {"id": uuid4(), "title": "Other", "description": "d",
             "scam_type": "phishing", "key_indicators": [], "similarity": 0.50},
        ]
    )

    result = await svc.match_and_record_pattern(db, "you are under digital arrest")

    assert result["recorded_match"]["id"] == str(pattern_id)
    # Only the top hit is counted, not every result above the threshold.
    update_params = db.execute.call_args[0][1]
    assert update_params["pattern_id"] == str(pattern_id)
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_match_and_record_pattern_ignores_weak_match():
    db = AsyncMock()
    db.execute.return_value = FakeResult(
        rows=[{"id": uuid4(), "title": "t", "description": "d", "scam_type": "phishing",
               "key_indicators": [], "similarity": 0.10}]
    )

    result = await svc.match_and_record_pattern(db, "unrelated text")

    assert result["recorded_match"] is None
    assert len(result["matches"]) == 1
    # A weak match must not inflate times_matched.
    db.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_match_and_record_pattern_no_matches():
    db = AsyncMock()
    db.execute.return_value = FakeResult(rows=[])
    result = await svc.match_and_record_pattern(db, "anything")
    assert result == {"matches": [], "recorded_match": None}
    db.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_backfill_embeddings_updates_missing():
    db = AsyncMock()
    db.execute.return_value = FakeResult(rows=[{"id": uuid4(), "description": "a"},
                                               {"id": uuid4(), "description": "b"}])
    count = await svc.backfill_embeddings(db)
    assert count == 2
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_backfill_embeddings_noop_when_all_embedded():
    db = AsyncMock()
    db.execute.return_value = FakeResult(rows=[])
    assert await svc.backfill_embeddings(db) == 0
    db.commit.assert_not_awaited()


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
