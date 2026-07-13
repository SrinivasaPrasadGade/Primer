"""Scam Sentinel: signal scoring, alert classification, script similarity, number reputation.

Yashi's logic layer — Srinivas's routers call process_scam_session()/get_session_detail()
and never touch signal internals directly.
"""

from __future__ import annotations

import asyncio
import json
from decimal import Decimal
import logging
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from uuid import UUID

import numpy as np
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

ML_MODELS_DIR = Path(__file__).resolve().parent.parent / "ml" / "models"
EMBED_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


@dataclass
class SignalResult:
    score: float  # 0.0-1.0
    explanation: str


def _to_jsonable(value):
    """Round-trip UUID/datetime/Decimal through JSON so they're plain str/float.

    Decimal must become a JSON number, not a string -- json.dumps(default=str) on its
    own stringifies Decimal, which silently breaks downstream numeric use (e.g. a
    Jinja "{:,.2f}".format(...) on a value that's now a str, or a risk_score/weight
    field that renders as "85" instead of 85 in an API response).
    """
    def _default(v):
        if isinstance(v, Decimal):
            return float(v)
        return str(v)

    return json.loads(json.dumps(value, default=_default))


# ---------------------------------------------------------------------------
# Alert classification
# ---------------------------------------------------------------------------

def classify_alert_level(overall_confidence: float) -> str:
    """RED >= 85, AMBER 60-84, YELLOW < 60.

    overall_confidence is on a 0-100 scale (matches scam_sessions.overall_confidence),
    NOT 0-1 — compare against 85/60, not 0.85/0.60.
    """
    if overall_confidence >= 85:
        return "RED"
    if overall_confidence >= 60:
        return "AMBER"
    return "YELLOW"


# ---------------------------------------------------------------------------
# Signal 2: Number spoofing — pure function, no I/O
# ---------------------------------------------------------------------------

def detect_number_spoofing(session_data: dict) -> SignalResult:
    caller_number = session_data.get("caller_number") or ""
    real_number = session_data.get("real_originating_number")
    spoofing_flagged = bool(session_data.get("spoofing_detected", False))

    if real_number and real_number != caller_number:
        return SignalResult(
            0.9,
            f"Caller ID {caller_number} is spoofed — true origin traced to {real_number}",
        )
    if spoofing_flagged:
        return SignalResult(0.7, "Spoofing indicators present but true origin unresolved")
    return SignalResult(0.0, "No spoofing indicators detected")


# ---------------------------------------------------------------------------
# Signal 5: Urgency phrase detection — pure function, no I/O
# ---------------------------------------------------------------------------

URGENCY_PHRASES = {
    "en": [
        "arrest warrant", "immediate transfer", "fir against you", "money laundering",
        "supreme court order", "digital arrest", "aadhaar linked", "account frozen",
        "non-bailable warrant", "customs seizure", "income tax notice",
    ],
    "hi": [
        "गिरफ्तारी वारंट", "तुरंत ट्रांसफर", "आपके खिलाफ एफआईआर", "मनी लॉन्ड्रिंग",
        "सुप्रीम कोर्ट का आदेश", "डिजिटल अरेस्ट", "आधार लिंक", "खाता फ्रीज",
    ],
}


def detect_urgency_phrases(text_content: str) -> SignalResult:
    if not text_content:
        return SignalResult(0.0, "No transcript available")

    lowered = text_content.lower()
    found = [phrase for phrases in URGENCY_PHRASES.values() for phrase in phrases if phrase in lowered]
    if not found:
        return SignalResult(0.0, "No urgency phrases detected")

    score = min(1.0, len(found) * 0.15 + 0.4)
    return SignalResult(score, f"Detected: {', '.join(found[:3])}")


# ---------------------------------------------------------------------------
# Signal 4: Voice synthetic probability — passthrough of VoiceSpoofDetector output,
# plus a live inference wrapper for when raw audio is available.
# ---------------------------------------------------------------------------

def _voice_explanation_from_probability(probability: float, deepfake_detected: bool = False) -> str:
    if deepfake_detected or probability >= 0.7:
        return f"VoiceSpoofDetector flags {probability * 100:.0f}% synthetic-voice probability"
    if probability >= 0.3:
        return f"Some synthetic-voice indicators ({probability * 100:.0f}%), inconclusive"
    return "Voice sample consistent with genuine human speech"


def generate_voice_explanation(session_data: dict) -> str:
    # voice_synthetic_probability is stored 0-1 (verified against seed data), not 0-100.
    # DB columns are NUMERIC/DECIMAL -> asyncpg returns Decimal, not float; normalize here
    # so downstream arithmetic (compute_signal_scores) never mixes Decimal with float.
    probability = float(session_data.get("voice_synthetic_probability") or 0)
    return _voice_explanation_from_probability(probability, bool(session_data.get("deepfake_detected")))


VOICE_SAMPLE_RATE = 16_000
VOICE_CLIP_SECONDS = 4
VOICE_N_MELS = 128
VOICE_N_FFT = 400  # 25ms @ 16kHz
VOICE_HOP_LENGTH = 160  # 10ms @ 16kHz


def _build_voice_spoof_model():
    """Construct the LCNN architecture from ml/voice-spoof-detector/train.py.

    Built lazily (not at import time) since it needs torch, which is only a hard
    dependency when live audio inference is actually used.
    """
    import torch
    import torch.nn as nn

    class MFM(nn.Module):
        def __init__(self, out_channels: int):
            super().__init__()
            self.out_channels = out_channels

        def forward(self, x):
            a, b = torch.split(x, self.out_channels, dim=1)
            return torch.max(a, b)

    class VoiceSpoofDetector(nn.Module):
        def __init__(self):
            super().__init__()
            self.features = nn.Sequential(
                nn.Conv2d(1, 64, 5, 1, 2), nn.MaxPool2d(2),
                nn.Conv2d(64, 64, 1, 1, 0), MFM(32),
                nn.Conv2d(32, 96, 3, 1, 1), nn.MaxPool2d(2),
                nn.Conv2d(96, 96, 1, 1, 0), MFM(48),
                nn.Conv2d(48, 128, 3, 1, 1), nn.MaxPool2d(2),
                nn.Conv2d(128, 128, 1, 1, 0), MFM(64),
            )
            self.classifier = nn.Sequential(
                nn.Linear(64 * 16 * 50, 256), nn.ReLU(), nn.Dropout(0.5),
                nn.Linear(256, 1),
            )

        def forward(self, x):
            x = self.features(x)
            x = x.view(x.size(0), -1)
            return torch.sigmoid(self.classifier(x))

    return VoiceSpoofDetector()


@lru_cache(maxsize=1)
def _load_voice_spoof_model():
    import torch

    model = _build_voice_spoof_model()
    state_dict = torch.load(ML_MODELS_DIR / "voice_spoof.pth", map_location="cpu", weights_only=True)
    model.load_state_dict(state_dict)
    model.eval()
    return model


def _audio_to_mel_spectrogram(audio_bytes: bytes) -> np.ndarray:
    """4s clip @ 16kHz -> 128x400 z-normalized log-mel spectrogram, matching training preprocessing."""
    import io

    import librosa

    audio, _ = librosa.load(io.BytesIO(audio_bytes), sr=VOICE_SAMPLE_RATE, mono=True)
    target_len = VOICE_SAMPLE_RATE * VOICE_CLIP_SECONDS
    if len(audio) < target_len:
        audio = np.pad(audio, (0, target_len - len(audio)))
    else:
        audio = audio[:target_len]

    mel = librosa.feature.melspectrogram(
        y=audio, sr=VOICE_SAMPLE_RATE, n_fft=VOICE_N_FFT, hop_length=VOICE_HOP_LENGTH, n_mels=VOICE_N_MELS
    )
    log_mel = librosa.power_to_db(mel, ref=np.max)
    return (log_mel - log_mel.mean()) / (log_mel.std() + 1e-8)


async def detect_voice_synthetic(audio_bytes: bytes) -> SignalResult:
    """Run VoiceSpoofDetector on a raw audio clip and return a synthetic-voice signal.

    Companion to generate_voice_explanation()/the voice_synthetic signal in
    compute_signal_scores(), for callers that have the raw call-audio clip rather than
    a value already stored on scam_sessions (e.g. the mobile app's live call screening).
    """
    try:
        model = _load_voice_spoof_model()
    except FileNotFoundError:
        return SignalResult(0.0, "VoiceSpoofDetector model unavailable")

    def _infer():
        import torch

        mel = _audio_to_mel_spectrogram(audio_bytes)
        tensor = torch.from_numpy(mel).float().unsqueeze(0).unsqueeze(0)  # (1, 1, 128, 400)
        with torch.no_grad():
            return float(model(tensor).item())

    probability = await asyncio.to_thread(_infer)
    return SignalResult(probability, _voice_explanation_from_probability(probability))


# ---------------------------------------------------------------------------
# Signal 3: Script similarity — prebuilt multilingual FAISS index
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _load_embedder():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBED_MODEL_NAME)


@lru_cache(maxsize=1)
def _load_corpus_index():
    """Load the FAISS index + row metadata the embedding pipeline already built.

    Loads the prebuilt artifacts (scam_corpus.faiss / scam_corpus_meta.json) rather
    than re-embedding scam_script_corpus from the DB on every cold start — that's a
    full round trip plus a full corpus re-embed for data that's already indexed.
    Falls back to (None, []) if the artifacts are missing so callers degrade gracefully.
    """
    import faiss

    index_path = ML_MODELS_DIR / "scam_corpus.faiss"
    meta_path = ML_MODELS_DIR / "scam_corpus_meta.json"
    if not index_path.exists() or not meta_path.exists():
        logger.warning("Scam corpus FAISS index not found at %s — script similarity disabled", index_path)
        return None, []

    index = faiss.read_index(str(index_path))
    rows = json.loads(meta_path.read_text(encoding="utf-8"))["rows"]
    return index, rows


async def compute_script_similarity(text_content: str) -> SignalResult:
    """Compare a transcript against the known scam-script corpus (cosine similarity)."""
    if not text_content:
        return SignalResult(0.0, "No transcript available")

    index, rows = _load_corpus_index()
    if index is None:
        return SignalResult(0.0, "Script corpus unavailable")

    def _search():
        embedder = _load_embedder()
        embedding = embedder.encode([text_content], normalize_embeddings=True).astype(np.float32)
        return index.search(embedding, 1)

    # Embedding + FAISS search are CPU-bound; offload so they don't block the event loop.
    scores, indices = await asyncio.to_thread(_search)
    top_idx = int(indices[0][0])
    if top_idx < 0 or top_idx >= len(rows):
        return SignalResult(0.0, "No corpus match found")

    match = rows[top_idx]
    top_score = max(0.0, min(1.0, float(scores[0][0])))
    return SignalResult(
        top_score,
        f"Matches \"{match['title']}\" ({match['scam_type']}) — {match['content'][:60]}...",
    )


# ---------------------------------------------------------------------------
# Signal 1: Call flow pattern match — trained XGBoost classifier on CDR features
# ---------------------------------------------------------------------------

CLASSIFIER_FEATURES = [
    "call_duration_sec", "caller_risk_score", "is_international_origin",
    "time_of_day_hour", "script_similarity_max", "urgency_phrase_count",
    "caller_complaint_count", "callee_age_group", "call_count_from_number_24h",
    "spoofing_indicator",
]


@lru_cache(maxsize=1)
def _load_classifier():
    import joblib

    model = joblib.load(ML_MODELS_DIR / "scam_classifier.joblib")
    age_encoder = joblib.load(ML_MODELS_DIR / "callee_age_group_encoder.joblib")
    return model, age_encoder


def _encode_age_group(age_encoder, age_group: str) -> int:
    try:
        return int(age_encoder.transform([age_group])[0])
    except ValueError:
        return int(age_encoder.transform([age_encoder.classes_[0]])[0])


def _build_classifier_features(session_data: dict, age_encoder) -> np.ndarray:
    call_start = session_data.get("call_start")
    hour = call_start.hour if isinstance(call_start, datetime) else session_data.get("time_of_day_hour", 12)
    caller_number = session_data.get("caller_number") or ""

    row = [
        session_data.get("call_duration_sec") or 0,
        session_data.get("caller_risk_score", 0),
        int(not caller_number.startswith("+91")) if caller_number else 0,
        hour,
        session_data.get("script_similarity_max", 0.0),
        session_data.get("urgency_phrase_count", 0),
        session_data.get("caller_complaint_count", 0),
        _encode_age_group(age_encoder, session_data.get("callee_age_group", "unknown")),
        session_data.get("call_count_from_number_24h", 0),
        int(bool(session_data.get("spoofing_detected", False))),
    ]
    return np.array([row], dtype=np.float32)


async def match_call_flow_pattern(session_data: dict) -> SignalResult:
    """Score the call's behavioural/CDR pattern with the trained XGBoost classifier.

    For the strongest prediction, pass an enriched session_data with caller_risk_score /
    caller_complaint_count / call_count_from_number_24h (from number_reputation) and
    script_similarity_max / urgency_phrase_count (from the other signals) — see
    compute_signal_scores(), which does this enrichment automatically. Any missing
    field defaults to 0/neutral so the signal still degrades gracefully.
    """
    try:
        model, age_encoder = _load_classifier()
    except FileNotFoundError:
        return SignalResult(0.0, "Scam classifier model unavailable")

    features = _build_classifier_features(session_data, age_encoder)
    probability = await asyncio.to_thread(lambda: float(model.predict_proba(features)[0][1]))

    if probability >= 0.7:
        explanation = "Call flow strongly matches known scam CDR patterns"
    elif probability >= 0.4:
        explanation = "Call flow partially matches scam CDR patterns"
    else:
        explanation = "Call flow consistent with normal calling behaviour"
    return SignalResult(probability, explanation)


# ---------------------------------------------------------------------------
# Orchestration: all 5 signals -> overall confidence -> alert level
# ---------------------------------------------------------------------------

SIGNAL_WEIGHTS = {
    "call_flow_match": 0.30,
    "number_spoofing": 0.15,
    "script_similarity": 0.20,
    "voice_synthetic": 0.20,
    "urgency_phrases": 0.15,
}


async def compute_signal_scores(session_data: dict) -> dict:
    """Compute all 5 signal scores for a scam session (drives Explainable AI).

    Returns {signal_name: {score, explanation}}. script_similarity and urgency_phrases
    run first and get folded back into the call-flow classifier's own feature vector
    (script_similarity_max, urgency_phrase_count) since the model was trained on those
    features — computing them up front gives a materially stronger call-flow signal
    than scoring on session metadata alone.
    """
    transcript = session_data.get("transcript_text", "")

    script_similarity = await compute_script_similarity(transcript)
    urgency_phrases = detect_urgency_phrases(transcript)
    urgency_count = urgency_phrases.explanation.count(",") + 1 if urgency_phrases.score > 0 else 0

    enriched = {
        **session_data,
        "script_similarity_max": script_similarity.score,
        "urgency_phrase_count": urgency_count,
    }

    call_flow_match = await match_call_flow_pattern(enriched)
    number_spoofing = detect_number_spoofing(session_data)
    voice_synthetic = SignalResult(
        score=float(session_data.get("voice_synthetic_probability") or 0),
        explanation=generate_voice_explanation(session_data),
    )

    signals = {
        "call_flow_match": call_flow_match,
        "number_spoofing": number_spoofing,
        "script_similarity": script_similarity,
        "voice_synthetic": voice_synthetic,
        "urgency_phrases": urgency_phrases,
    }
    return {name: {"score": round(s.score, 2), "explanation": s.explanation} for name, s in signals.items()}


def compute_overall_confidence(signals: dict) -> float:
    """Weighted blend of the 5 signal scores -> 0-100 scale (matches the DB column)."""
    total = sum(signals[name]["score"] * weight for name, weight in SIGNAL_WEIGHTS.items() if name in signals)
    return round(min(100.0, total * 100), 2)


# ---------------------------------------------------------------------------
# Number reputation
# ---------------------------------------------------------------------------

def _phone_suffix(value: str) -> str:
    """Last 10 digits of a phone number, ignoring +, country code, spaces, and dashes,
    so reputation lookups aren't defeated by formatting differences."""
    digits = "".join(ch for ch in (value or "") if ch.isdigit())
    return digits[-10:]


async def get_number_reputation(db: AsyncSession, phone_number: str) -> dict | None:
    row = (
        await db.execute(
            text(
                "SELECT * FROM scam_sentinel.number_reputation "
                "WHERE RIGHT(regexp_replace(phone_number, '\\D', '', 'g'), 10) = :suffix"
            ),
            {"suffix": _phone_suffix(phone_number)},
        )
    ).mappings().first()
    return dict(row) if row else None


async def update_number_reputation(db: AsyncSession, phone_number: str, alert_level: str) -> dict:
    """Upsert a number's reputation after a session is classified.

    risk_score climbs with flag frequency and severity, capped at 100 — a RED session
    weighs more than AMBER/YELLOW since it reflects much higher model confidence.
    """
    severity_bump = {"RED": 25, "AMBER": 12, "YELLOW": 4, "NONE": 0}.get(alert_level, 0)
    is_scam_flag = int(alert_level in ("RED", "AMBER"))

    row = (
        await db.execute(
            text(
                """
                INSERT INTO scam_sentinel.number_reputation
                    (phone_number, risk_score, total_flags, total_complaints, last_flagged, updated_at)
                VALUES (:phone, :bump, 1, :complaint, NOW(), NOW())
                ON CONFLICT (phone_number) DO UPDATE SET
                    risk_score = LEAST(100, scam_sentinel.number_reputation.risk_score + :bump),
                    total_flags = scam_sentinel.number_reputation.total_flags + 1,
                    total_complaints = scam_sentinel.number_reputation.total_complaints + :complaint,
                    last_flagged = NOW(),
                    updated_at = NOW()
                RETURNING *
                """
            ),
            {"phone": phone_number, "bump": severity_bump, "complaint": is_scam_flag},
        )
    ).mappings().first()
    await db.commit()
    return dict(row)


# ---------------------------------------------------------------------------
# Session fetch / processing — the entry points Srinivas's routers call
# ---------------------------------------------------------------------------

_SESSION_COLUMNS = """
    id, caller_number, callee_number, call_start, call_end,
    call_duration_sec, alert_level, overall_confidence, scam_type,
    scam_phase, signal_scores, spoofing_detected,
    real_originating_number, deepfake_detected,
    voice_synthetic_probability, status, created_at, updated_at
"""


async def _fetch_session(db: AsyncSession, session_id: UUID) -> dict | None:
    row = (
        await db.execute(
            text(f"SELECT {_SESSION_COLUMNS} FROM scam_sentinel.scam_sessions WHERE id = :session_id"),
            {"session_id": session_id},
        )
    ).mappings().first()
    return dict(row) if row else None


async def process_scam_session(db: AsyncSession, session_id: UUID) -> dict:
    """Score a scam session end-to-end: compute signals, classify, persist, and
    update the caller number's reputation. Main entry point for Srinivas's routers.
    """
    session = await _fetch_session(db, session_id)
    if not session:
        raise ValueError(f"Scam session {session_id} not found")

    caller_reputation = await get_number_reputation(db, session["caller_number"])
    enriched = {
        **session,
        "caller_risk_score": caller_reputation["risk_score"] if caller_reputation else 0,
        "caller_complaint_count": caller_reputation["total_complaints"] if caller_reputation else 0,
        "call_count_from_number_24h": caller_reputation["total_flags"] if caller_reputation else 0,
    }

    signals = await compute_signal_scores(enriched)
    overall_confidence = compute_overall_confidence(signals)
    alert_level = classify_alert_level(overall_confidence)

    await db.execute(
        text(
            """
            UPDATE scam_sentinel.scam_sessions
            SET signal_scores = CAST(:signals AS JSONB), overall_confidence = :confidence,
                alert_level = :alert_level, status = 'classified', updated_at = NOW()
            WHERE id = :session_id
            """
        ),
        {
            "signals": json.dumps(signals),
            "confidence": overall_confidence,
            "alert_level": alert_level,
            "session_id": session_id,
        },
    )
    await db.commit()
    # NOTE: reputation is deliberately NOT bumped here. Classification must be
    # idempotent — re-running it on the same session should yield identical scores.
    # Auto-bumping risk_score fed back into the classifier's caller_risk_score feature,
    # so every re-run drifted. Reputation is updated explicitly via /numbers/{phone}/flag.

    return {
        "session_id": str(session_id),
        "alert_level": alert_level,
        "overall_confidence": overall_confidence,
        "signal_scores": signals,
    }


async def get_session_detail(db: AsyncSession, session_id: UUID) -> dict | None:
    """Fetch a session with its stored signal_scores, ready for Explainable AI display."""
    session = await _fetch_session(db, session_id)
    if not session:
        return None
    session["signal_scores"] = session.get("signal_scores") or {}
    return _to_jsonable(session)
