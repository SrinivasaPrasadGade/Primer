"""Unit tests for app.services.note_verify — mocked model/AsyncSession, no live Postgres/torch needed."""

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.services import note_verify as svc


class FakeResult:
    def __init__(self, row=None):
        self._row = row

    def mappings(self):
        return self

    def first(self):
        return self._row


# ---------------------------------------------------------------------------
# classify_verdict
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "overall_score,is_known_counterfeit,expected",
    [
        (0.95, False, "GENUINE"),
        (0.7, False, "GENUINE"),
        (0.69, False, "SUSPECT"),
        (0.4, False, "SUSPECT"),
        (0.39, False, "COUNTERFEIT"),
        (0.0, False, "COUNTERFEIT"),
        (0.99, True, "COUNTERFEIT"),  # known-serial match overrides a high image score
    ],
)
def test_classify_verdict(overall_score, is_known_counterfeit, expected):
    assert svc.classify_verdict(overall_score, is_known_counterfeit) == expected


# ---------------------------------------------------------------------------
# analyze_note_image — degrade gracefully without the model file
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_analyze_note_image_model_missing(monkeypatch):
    """When the trained weights are unavailable (e.g. Git LFS not pulled), the service
    must degrade to the deterministic heuristic instead of raising a 500."""
    def _raise():
        raise FileNotFoundError

    monkeypatch.setattr(svc, "_load_note_auth_net", _raise)
    result = await svc.analyze_note_image(b"irrelevant bytes")

    # Heuristic keys match, scores land in the plausible-genuine band, and are stable.
    assert set(result.keys()) == set(svc.FEATURE_NAMES)
    assert all(0.55 <= v <= 0.98 for v in result.values())
    assert result == await svc.analyze_note_image(b"irrelevant bytes")


@pytest.mark.asyncio
async def test_analyze_note_image_with_model(monkeypatch):
    class FakeTensor:
        def squeeze(self, dim):
            return self

        def tolist(self):
            return [0.9, 0.8, 0.7, 0.6, 0.5, 0.85]

    class FakeModel:
        def __call__(self, tensor):
            return FakeTensor()

    monkeypatch.setattr(svc, "_load_note_auth_net", lambda: FakeModel())
    monkeypatch.setattr(svc, "_preprocess_image", lambda image_bytes: __import__("numpy").zeros((3, 380, 380)))

    result = await svc.analyze_note_image(b"irrelevant bytes")

    assert result["overall"] == 0.85
    assert set(result.keys()) == set(svc.FEATURE_NAMES)


# ---------------------------------------------------------------------------
# check_counterfeit_serial
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_check_counterfeit_serial_found():
    db = AsyncMock()
    db.execute.return_value = FakeResult(row={"serial_number": "ABC123", "denomination": 500, "detection_count": 3})
    result = await svc.check_counterfeit_serial(db, "ABC123")
    assert result["detection_count"] == 3


@pytest.mark.asyncio
async def test_check_counterfeit_serial_not_found():
    db = AsyncMock()
    db.execute.return_value = FakeResult(row=None)
    result = await svc.check_counterfeit_serial(db, "XYZ999")
    assert result is None


@pytest.mark.asyncio
async def test_check_counterfeit_serial_empty_string():
    db = AsyncMock()
    result = await svc.check_counterfeit_serial(db, "")
    assert result is None
    db.execute.assert_not_called()


# ---------------------------------------------------------------------------
# verify_note — full pipeline with mocked model + mocked DB
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_verify_note_genuine(monkeypatch):
    async def fake_analyze(image_bytes):
        return {"watermark": 0.9, "thread": 0.9, "microprint": 0.9, "intaglio": 0.9, "colour_shift": 0.9, "overall": 0.9}

    monkeypatch.setattr(svc, "analyze_note_image", fake_analyze)

    async def fake_check(db, serial_number):
        return None  # not previously known

    monkeypatch.setattr(svc, "check_counterfeit_serial", fake_check)

    verification_id = uuid4()
    db = AsyncMock()
    db.execute.return_value = FakeResult(
        row={
            "id": verification_id, "user_id": None, "denomination": 500, "serial_number": "GEN001",
            "verdict": "GENUINE", "confidence": 90.0, "feature_analysis": {}, "scan_source": "mobile",
            "is_known_counterfeit": False, "created_at": None,
        }
    )

    result = await svc.verify_note(db, b"image bytes", denomination=500, serial_number="GEN001")

    assert result["verdict"] == "GENUINE"
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_verify_note_counterfeit_records_serial(monkeypatch):
    async def fake_analyze(image_bytes):
        return {"watermark": 0.1, "thread": 0.1, "microprint": 0.1, "intaglio": 0.1, "colour_shift": 0.1, "overall": 0.1}

    monkeypatch.setattr(svc, "analyze_note_image", fake_analyze)

    record_calls = []

    async def fake_check(db, serial_number):
        return None  # not previously known

    async def fake_record(db, serial_number, denomination):
        record_calls.append((serial_number, denomination))

    monkeypatch.setattr(svc, "check_counterfeit_serial", fake_check)
    monkeypatch.setattr(svc, "record_counterfeit_serial", fake_record)

    db = AsyncMock()
    db.execute.return_value = FakeResult(
        row={
            "id": uuid4(), "user_id": None, "denomination": 2000, "serial_number": "FAKE999",
            "verdict": "COUNTERFEIT", "confidence": 90.0, "feature_analysis": {}, "scan_source": "mobile",
            "is_known_counterfeit": False, "created_at": None,
        }
    )

    await svc.verify_note(db, b"image bytes", denomination=2000, serial_number="FAKE999")

    assert record_calls == [("FAKE999", 2000)]


@pytest.mark.asyncio
async def test_verify_note_known_counterfeit_skips_re_recording(monkeypatch):
    async def fake_analyze(image_bytes):
        return {"watermark": 0.1, "thread": 0.1, "microprint": 0.1, "intaglio": 0.1, "colour_shift": 0.1, "overall": 0.1}

    async def fake_check(db, serial_number):
        return {"serial_number": serial_number, "denomination": 500, "detection_count": 5}

    record_calls = []

    async def fake_record(db, serial_number, denomination):
        record_calls.append((serial_number, denomination))

    monkeypatch.setattr(svc, "analyze_note_image", fake_analyze)
    monkeypatch.setattr(svc, "check_counterfeit_serial", fake_check)
    monkeypatch.setattr(svc, "record_counterfeit_serial", fake_record)

    db = AsyncMock()
    db.execute.return_value = FakeResult(
        row={
            "id": uuid4(), "user_id": None, "denomination": 500, "serial_number": "KNOWN1",
            "verdict": "COUNTERFEIT", "confidence": 90.0, "feature_analysis": {}, "scan_source": "mobile",
            "is_known_counterfeit": True, "created_at": None,
        }
    )

    await svc.verify_note(db, b"image bytes", denomination=500, serial_number="KNOWN1")

    assert record_calls == []  # already known, no duplicate-recording call


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_verification_stats():
    db = AsyncMock()
    db.execute.return_value = FakeResult(
        row={"total_scans": 10, "genuine_count": 6, "suspect_count": 2, "counterfeit_count": 2}
    )
    result = await svc.get_verification_stats(db)
    assert result["total_scans"] == 10
