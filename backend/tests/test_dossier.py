"""Unit tests for app.services.dossier — mocked AsyncSession, no live Postgres/WeasyPrint render needed."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.services import dossier as svc


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


@pytest.mark.asyncio
async def test_get_cluster_data_found():
    cluster_id = uuid4()
    db = AsyncMock()
    db.execute.return_value = FakeResult(row={"id": cluster_id, "name": "Test Cluster", "node_count": 5,
                                               "edge_count": 8, "estimated_loss": 100000.0, "victim_count": 3,
                                               "status": "active", "detected_at": None})
    result = await svc.get_cluster_data(db, cluster_id)
    assert result["name"] == "Test Cluster"


@pytest.mark.asyncio
async def test_get_cluster_data_not_found():
    db = AsyncMock()
    db.execute.return_value = FakeResult(row=None)
    result = await svc.get_cluster_data(db, uuid4())
    assert result is None


@pytest.mark.asyncio
async def test_get_cluster_timeline_sorted(monkeypatch):
    async def fake_entities(db, cluster_id):
        return [{"entity_type": "phone_number", "entity_value": "+91123", "first_seen": "2026-02-01"}]

    async def fake_edges(db, cluster_id):
        return [{"source_label": "+91123", "relationship": "linked_to", "target_label": "x@ybl",
                  "first_seen": "2026-01-01"}]

    monkeypatch.setattr(svc, "get_cluster_entities", fake_entities)
    monkeypatch.setattr(svc, "get_cluster_edges", fake_edges)

    timeline = await svc.get_cluster_timeline(AsyncMock(), uuid4())

    assert len(timeline) == 2
    assert timeline[0]["date"] == "2026-01-01"  # earliest event first
    assert timeline[1]["date"] == "2026-02-01"


@pytest.mark.asyncio
async def test_generate_dossier_cluster_not_found(monkeypatch):
    async def fake_get_cluster_data(db, cluster_id):
        return None

    monkeypatch.setattr(svc, "get_cluster_data", fake_get_cluster_data)
    with pytest.raises(ValueError):
        await svc.generate_dossier(AsyncMock(), uuid4(), uuid4())


@pytest.mark.asyncio
async def test_generate_dossier_happy_path(monkeypatch, tmp_path):
    cluster_id = uuid4()
    officer_id = uuid4()

    async def fake_get_cluster_data(db, cid):
        return {"id": cluster_id, "name": "Test Cluster", "node_count": 1, "edge_count": 0,
                "estimated_loss": 5000.0, "victim_count": 1, "status": "active"}

    async def fake_entities(db, cid):
        return [{"entity_type": "upi_id", "entity_value": "x@ybl", "display_label": None, "risk_score": 90}]

    async def fake_edges(db, cid):
        return []

    async def fake_timeline(db, cid):
        return [{"date": "2026-01-01", "event": "First observed"}]

    monkeypatch.setattr(svc, "get_cluster_data", fake_get_cluster_data)
    monkeypatch.setattr(svc, "get_cluster_entities", fake_entities)
    monkeypatch.setattr(svc, "get_cluster_edges", fake_edges)
    monkeypatch.setattr(svc, "get_cluster_timeline", fake_timeline)
    monkeypatch.setattr(svc, "DOSSIERS_DIR", tmp_path)

    db = AsyncMock()
    output_path = await svc.generate_dossier(db, cluster_id, officer_id)

    assert str(tmp_path) in output_path
    assert output_path.endswith(".pdf")
    db.commit.assert_awaited_once()
    db.execute.assert_awaited_once()
