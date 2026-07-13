"""Unit tests for app.services.scam_sentinel — pure-logic + mocked-DB, no live Postgres/FAISS/model files needed."""

from datetime import datetime
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.services import scam_sentinel as svc


class FakeResult:
    """Mimics SQLAlchemy's Result: .mappings().first() / .all()."""

    def __init__(self, row=None, rows=None):
        self._row = row
        self._rows = rows or []

    def mappings(self):
        return self

    def first(self):
        return self._row

    def all(self):
        return self._rows


# ---------------------------------------------------------------------------
# Alert classification
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "confidence,expected",
    [(99, "RED"), (85, "RED"), (84.9, "AMBER"), (60, "AMBER"), (59.9, "YELLOW"), (0, "YELLOW")],
)
def test_classify_alert_level(confidence, expected):
    assert svc.classify_alert_level(confidence) == expected


# ---------------------------------------------------------------------------
# Number spoofing
# ---------------------------------------------------------------------------

def test_detect_number_spoofing_real_number_mismatch():
    result = svc.detect_number_spoofing(
        {"caller_number": "+911234567890", "real_originating_number": "+861112223333"}
    )
    assert result.score == 0.9
    assert "spoofed" in result.explanation


def test_detect_number_spoofing_flag_only():
    result = svc.detect_number_spoofing({"caller_number": "+911234567890", "spoofing_detected": True})
    assert result.score == 0.7


def test_detect_number_spoofing_clean():
    result = svc.detect_number_spoofing({"caller_number": "+911234567890"})
    assert result.score == 0.0


# ---------------------------------------------------------------------------
# Urgency phrases
# ---------------------------------------------------------------------------

def test_detect_urgency_phrases_english():
    result = svc.detect_urgency_phrases("This is your digital arrest, an FIR against you is filed.")
    assert result.score > 0
    assert "digital arrest" in result.explanation


def test_detect_urgency_phrases_hindi():
    result = svc.detect_urgency_phrases("आपके खिलाफ एफआईआर दर्ज है, गिरफ्तारी वारंट जारी हो चुका है।")
    assert result.score > 0


def test_detect_urgency_phrases_none():
    result = svc.detect_urgency_phrases("Hi, just calling to check in on the weather today.")
    assert result.score == 0.0


def test_detect_urgency_phrases_empty():
    result = svc.detect_urgency_phrases("")
    assert result.score == 0.0
    assert result.explanation == "No transcript available"


# ---------------------------------------------------------------------------
# Voice synthetic explanation
# ---------------------------------------------------------------------------

def test_generate_voice_explanation_high():
    # voice_synthetic_probability is stored 0-1 (verified against real seed data), not 0-100
    assert "synthetic" in svc.generate_voice_explanation({"voice_synthetic_probability": 0.92})


def test_generate_voice_explanation_genuine():
    assert "genuine" in svc.generate_voice_explanation({"voice_synthetic_probability": 0.05})


# ---------------------------------------------------------------------------
# Deepfake voice inference wrapper — degrade gracefully without the model file
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_detect_voice_synthetic_model_missing(monkeypatch):
    def _raise():
        raise FileNotFoundError

    monkeypatch.setattr(svc, "_load_voice_spoof_model", _raise)
    result = await svc.detect_voice_synthetic(b"irrelevant audio bytes")
    assert result.score == 0.0
    assert result.explanation == "VoiceSpoofDetector model unavailable"


@pytest.mark.asyncio
async def test_detect_voice_synthetic_with_model(monkeypatch):
    import numpy as np

    class FakeModel:
        def __call__(self, tensor):
            class FakeTensor:
                def item(self):
                    return 0.87

            return FakeTensor()

    monkeypatch.setattr(svc, "_load_voice_spoof_model", lambda: FakeModel())
    monkeypatch.setattr(svc, "_audio_to_mel_spectrogram", lambda audio_bytes: np.zeros((128, 400), dtype="float32"))

    result = await svc.detect_voice_synthetic(b"irrelevant audio bytes")

    assert result.score == pytest.approx(0.87)
    assert "flags" in result.explanation


def test_voice_explanation_from_probability_thresholds():
    assert "genuine" in svc._voice_explanation_from_probability(0.1)
    assert "inconclusive" in svc._voice_explanation_from_probability(0.5)
    assert "flags" in svc._voice_explanation_from_probability(0.9)
    assert "flags" in svc._voice_explanation_from_probability(0.1, deepfake_detected=True)


# ---------------------------------------------------------------------------
# Script similarity — degrade gracefully without the FAISS artifacts
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_compute_script_similarity_no_index(monkeypatch):
    monkeypatch.setattr(svc, "_load_corpus_index", lambda: (None, []))
    result = await svc.compute_script_similarity("some transcript text")
    assert result.score == 0.0
    assert result.explanation == "Script corpus unavailable"


@pytest.mark.asyncio
async def test_compute_script_similarity_empty_text():
    result = await svc.compute_script_similarity("")
    assert result.score == 0.0


@pytest.mark.asyncio
async def test_compute_script_similarity_with_match(monkeypatch):
    class FakeIndex:
        def search(self, embedding, k):
            import numpy as np

            return np.array([[0.87]]), np.array([[0]])

    rows = [{"title": "Customs Seizure Scam", "scam_type": "customs_seizure", "content": "pay penalty now"}]
    monkeypatch.setattr(svc, "_load_corpus_index", lambda: (FakeIndex(), rows))

    class FakeEmbedder:
        def encode(self, texts, normalize_embeddings=True):
            import numpy as np

            return np.zeros((1, 384), dtype="float32")

    monkeypatch.setattr(svc, "_load_embedder", lambda: FakeEmbedder())

    result = await svc.compute_script_similarity("customs seizure, pay now")
    assert result.score == pytest.approx(0.87)
    assert "Customs Seizure Scam" in result.explanation


# ---------------------------------------------------------------------------
# Call flow pattern match — degrade gracefully without the model file
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_match_call_flow_pattern_model_missing(monkeypatch):
    def _raise():
        raise FileNotFoundError

    monkeypatch.setattr(svc, "_load_classifier", _raise)
    result = await svc.match_call_flow_pattern({"call_duration_sec": 120})
    assert result.score == 0.0
    assert result.explanation == "Scam classifier model unavailable"


@pytest.mark.asyncio
async def test_match_call_flow_pattern_with_model(monkeypatch):
    class FakeModel:
        def predict_proba(self, features):
            return [[0.1, 0.82]]

    class FakeEncoder:
        classes_ = ["unknown", "senior"]

        def transform(self, values):
            return [1 if values[0] == "senior" else 0]

    monkeypatch.setattr(svc, "_load_classifier", lambda: (FakeModel(), FakeEncoder()))

    result = await svc.match_call_flow_pattern(
        {"call_duration_sec": 300, "caller_number": "+911234567890", "callee_age_group": "senior"}
    )
    assert result.score == pytest.approx(0.82)
    assert "strongly matches" in result.explanation


# ---------------------------------------------------------------------------
# Overall confidence weighting
# ---------------------------------------------------------------------------

def test_compute_overall_confidence():
    signals = {
        "call_flow_match": {"score": 1.0},
        "number_spoofing": {"score": 1.0},
        "script_similarity": {"score": 1.0},
        "voice_synthetic": {"score": 1.0},
        "urgency_phrases": {"score": 1.0},
    }
    assert svc.compute_overall_confidence(signals) == 100.0


def test_compute_overall_confidence_partial():
    signals = {
        "call_flow_match": {"score": 0.0},
        "number_spoofing": {"score": 0.0},
        "script_similarity": {"score": 0.0},
        "voice_synthetic": {"score": 0.0},
        "urgency_phrases": {"score": 0.0},
    }
    assert svc.compute_overall_confidence(signals) == 0.0


# ---------------------------------------------------------------------------
# compute_signal_scores — full orchestration with mocked heavy dependencies
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_compute_signal_scores(monkeypatch):
    async def fake_script_similarity(text_content):
        return svc.SignalResult(0.8, "Matches template")

    async def fake_call_flow(session_data):
        assert session_data["script_similarity_max"] == 0.8
        assert session_data["urgency_phrase_count"] >= 1
        return svc.SignalResult(0.75, "Call flow matches")

    monkeypatch.setattr(svc, "compute_script_similarity", fake_script_similarity)
    monkeypatch.setattr(svc, "match_call_flow_pattern", fake_call_flow)

    session_data = {
        "transcript_text": "This is a digital arrest, immediate transfer required.",
        "caller_number": "+911234567890",
        "real_originating_number": "+861112223333",
        "voice_synthetic_probability": 0.8,
        "deepfake_detected": True,
    }
    signals = await svc.compute_signal_scores(session_data)

    assert set(signals) == {"call_flow_match", "number_spoofing", "script_similarity", "voice_synthetic", "urgency_phrases"}
    assert signals["call_flow_match"]["score"] == 0.75
    assert signals["number_spoofing"]["score"] == 0.9
    assert signals["voice_synthetic"]["score"] == 0.8


# ---------------------------------------------------------------------------
# Number reputation — mocked AsyncSession
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_number_reputation_found():
    db = AsyncMock()
    db.execute.return_value = FakeResult(row={"phone_number": "+911234567890", "risk_score": 40})
    result = await svc.get_number_reputation(db, "+911234567890")
    assert result["risk_score"] == 40


@pytest.mark.asyncio
async def test_get_number_reputation_not_found():
    db = AsyncMock()
    db.execute.return_value = FakeResult(row=None)
    result = await svc.get_number_reputation(db, "+919999999999")
    assert result is None


@pytest.mark.asyncio
async def test_update_number_reputation():
    db = AsyncMock()
    db.execute.return_value = FakeResult(row={"phone_number": "+911234567890", "risk_score": 25, "total_flags": 1})
    result = await svc.update_number_reputation(db, "+911234567890", "RED")
    db.commit.assert_awaited_once()
    assert result["risk_score"] == 25
    call_args = db.execute.call_args
    assert call_args[0][1]["bump"] == 25


# ---------------------------------------------------------------------------
# process_scam_session — full pipeline with mocked DB + mocked signal computation
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_process_scam_session_not_found():
    db = AsyncMock()
    db.execute.return_value = FakeResult(row=None)
    with pytest.raises(ValueError):
        await svc.process_scam_session(db, uuid4())


@pytest.mark.asyncio
async def test_process_scam_session_happy_path(monkeypatch):
    session_id = uuid4()
    session_row = {
        "id": session_id,
        "caller_number": "+911234567890",
        "callee_number": "+919876543210",
        "call_start": datetime(2026, 7, 8, 11, 0, 0),
        "transcript_text": "digital arrest, immediate transfer",
        "voice_synthetic_probability": 0.9,
        "spoofing_detected": True,
        "real_originating_number": "+861112223333",
    }
    reputation_row = {"phone_number": "+911234567890", "risk_score": 50, "total_complaints": 3, "total_flags": 5}

    db = AsyncMock()
    # execute() is called 3 times: fetch session, fetch reputation, update session.
    # Reputation is NOT upserted during classify (classification must stay idempotent).
    db.execute.side_effect = [
        FakeResult(row=session_row),
        FakeResult(row=reputation_row),
        FakeResult(row=None),
    ]

    async def fake_compute_signal_scores(enriched):
        assert enriched["caller_risk_score"] == 50
        return {
            "call_flow_match": {"score": 0.9, "explanation": "x"},
            "number_spoofing": {"score": 0.9, "explanation": "x"},
            "script_similarity": {"score": 0.9, "explanation": "x"},
            "voice_synthetic": {"score": 0.9, "explanation": "x"},
            "urgency_phrases": {"score": 0.9, "explanation": "x"},
        }

    monkeypatch.setattr(svc, "compute_signal_scores", fake_compute_signal_scores)

    result = await svc.process_scam_session(db, session_id)

    assert result["alert_level"] == "RED"
    assert result["overall_confidence"] == 90.0
    assert db.commit.await_count == 1
