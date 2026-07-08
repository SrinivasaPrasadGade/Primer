"""Unit tests for app.services.case_summary — mocked fraud_graph/Gemini/AsyncSession, no live Postgres/Gemini needed."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.services import case_summary as svc
from app.services.gemini_client import GeminiError


class FakeResult:
    def __init__(self, row=None):
        self._row = row

    def mappings(self):
        return self

    def first(self):
        return self._row


# ---------------------------------------------------------------------------
# extract_evidence
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_extract_evidence_no_nodes(monkeypatch):
    async def fake_neighbourhood(db, entity_type, entity_value, depth=2):
        return {"nodes": [], "edges": []}

    monkeypatch.setattr(svc.fraud_graph, "get_entity_neighbourhood", fake_neighbourhood)
    db = AsyncMock()

    result = await svc.extract_evidence(db, "phone_number", "+911234567890")

    assert "Connected entities (0)" in result
    assert "Money flow" not in result


@pytest.mark.asyncio
async def test_extract_evidence_with_nodes_and_money_flow(monkeypatch):
    node_id = str(uuid4())
    graph = {
        "nodes": [{"id": node_id, "entity_type": "upi_id", "entity_value": "x@ybl", "risk_score": 80}],
        "edges": [{"source_id": "a", "target_id": "b", "relationship": "linked_to", "weight": 1.0,
                   "source_label": "+911234567890", "target_label": "x@ybl"}],
    }
    money_flow = [{"from_entity": "acc1", "to_entity": "acc2", "amount": 50000.0}]

    async def fake_neighbourhood(db, entity_type, entity_value, depth=2):
        return graph

    async def fake_money_flow(db, entity_id):
        assert str(entity_id) == node_id
        return money_flow

    monkeypatch.setattr(svc.fraud_graph, "get_entity_neighbourhood", fake_neighbourhood)
    monkeypatch.setattr(svc.fraud_graph, "get_money_flow", fake_money_flow)

    db = AsyncMock()
    result = await svc.extract_evidence(db, "phone_number", "+911234567890")

    assert "Connected entities (1)" in result
    assert "Connections (1)" in result
    assert "Money flow (1 transfers)" in result
    assert "acc1 -> acc2: 50000.0" in result


# ---------------------------------------------------------------------------
# generate_case_summary
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_generate_case_summary_success(monkeypatch):
    expected = {"summary": "test", "timeline": [], "suspects": [], "related_complaints": [], "confidence_score": 80}

    async def fake_generate_json(prompt, system_instruction=None):
        return expected

    monkeypatch.setattr(svc, "generate_json", fake_generate_json)
    result = await svc.generate_case_summary("some evidence text")
    assert result == expected


@pytest.mark.asyncio
async def test_generate_case_summary_gemini_error_degrades(monkeypatch):
    async def fake_generate_json(prompt, system_instruction=None):
        raise GeminiError("no API key")

    monkeypatch.setattr(svc, "generate_json", fake_generate_json)
    result = await svc.generate_case_summary("some evidence text")
    assert result["confidence_score"] == 0
    assert result["timeline"] == []


@pytest.mark.asyncio
async def test_generate_case_summary_bad_json_degrades(monkeypatch):
    import json

    async def fake_generate_json(prompt, system_instruction=None):
        raise json.JSONDecodeError("bad", "doc", 0)

    monkeypatch.setattr(svc, "generate_json", fake_generate_json)
    result = await svc.generate_case_summary("some evidence text")
    assert "manual review" in result["summary"]


# ---------------------------------------------------------------------------
# summarize_and_store
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_summarize_and_store(monkeypatch):
    async def fake_extract_evidence(db, entity_type, entity_value):
        return "evidence text"

    async def fake_generate_case_summary(evidence_text):
        return {
            "summary": "A fraud ring was identified.",
            "timeline": [{"date": "2026-01-01", "event": "First complaint"}],
            "suspects": [{"identifier": "x@ybl", "type": "upi_id", "role": "recipient", "risk_score": 90}],
            "related_complaints": ["C001"],
            "confidence_score": 75,
        }

    monkeypatch.setattr(svc, "extract_evidence", fake_extract_evidence)
    monkeypatch.setattr(svc, "generate_case_summary", fake_generate_case_summary)

    summary_id = uuid4()
    generated_by = uuid4()
    db = AsyncMock()
    db.execute.return_value = FakeResult(
        row={
            "id": summary_id, "investigation_id": None, "summary_text": "A fraud ring was identified.",
            "timeline_json": [{"date": "2026-01-01", "event": "First complaint"}],
            "suspects_json": [{"identifier": "x@ybl", "type": "upi_id", "role": "recipient", "risk_score": 90}],
            "related_complaints": ["C001"], "confidence_score": 75,
            "source_evidence": ["upi_id:x@ybl"], "generated_by": generated_by, "created_at": None,
        }
    )

    result = await svc.summarize_and_store(db, "upi_id", "x@ybl", generated_by)

    assert result["id"] == str(summary_id)
    assert result["confidence_score"] == 75
    db.commit.assert_awaited_once()
    params = db.execute.call_args[0][1]
    assert params["source_evidence"] == ["upi_id:x@ybl"]
