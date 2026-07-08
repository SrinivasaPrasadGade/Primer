"""Note Verify: currency counterfeit detection (NoteAuthNet inference) + serial lookup.

Yashi's logic layer — Srinivas's routers call verify_note() as the entry point.
"""

from __future__ import annotations

import asyncio
import json
from decimal import Decimal
from functools import lru_cache
from pathlib import Path
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

ML_MODELS_DIR = Path(__file__).resolve().parent.parent / "ml" / "models"

FEATURE_NAMES = ["watermark", "thread", "microprint", "intaglio", "colour_shift", "overall"]
NOTE_IMAGE_SIZE = 380  # EfficientNet-B4's native input resolution
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

VERDICT_GENUINE_THRESHOLD = 0.7
VERDICT_SUSPECT_THRESHOLD = 0.4


def _to_jsonable(value):
    """Round-trip UUID/datetime/Decimal through JSON so they're plain str/float.

    Decimal must become a JSON number, not a string -- json.dumps(default=str) on its
    own stringifies Decimal, which silently breaks downstream numeric use.
    """
    def _default(v):
        if isinstance(v, Decimal):
            return float(v)
        return str(v)

    return json.loads(json.dumps(value, default=_default))


# ---------------------------------------------------------------------------
# NoteAuthNet — EfficientNet-B4 backbone, 6-head output (real trained weights)
# ---------------------------------------------------------------------------

def _build_note_auth_net():
    """Construct the multi-head architecture from ml/note-auth-net/train.py.

    Built lazily (not at import time) since it needs torch/timm, which are only a
    hard dependency when live image inference is actually used.
    """
    import timm
    import torch.nn as nn

    class NoteAuthNet(nn.Module):
        def __init__(self, num_features=6):
            super().__init__()
            self.backbone = timm.create_model("efficientnet_b4", pretrained=False, num_classes=0)
            feature_dim = self.backbone.num_features
            self.heads = nn.ModuleList(
                [
                    nn.Sequential(nn.Linear(feature_dim, 256), nn.ReLU(), nn.Dropout(0.3), nn.Linear(256, 1))
                    for _ in range(num_features)
                ]
            )

        def forward(self, x):
            import torch

            features = self.backbone(x)
            logits = torch.cat([head(features) for head in self.heads], dim=1)
            return torch.sigmoid(logits)

    return NoteAuthNet()


@lru_cache(maxsize=1)
def _load_note_auth_net():
    import torch

    model = _build_note_auth_net()
    state_dict = torch.load(ML_MODELS_DIR / "note_auth_net.pth", map_location="cpu", weights_only=True)
    model.load_state_dict(state_dict)
    model.eval()
    return model


def _preprocess_image(image_bytes: bytes):
    """Decode + resize to 380x380 + ImageNet-normalize, matching training preprocessing."""
    import io

    import numpy as np
    from PIL import Image

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((NOTE_IMAGE_SIZE, NOTE_IMAGE_SIZE))
    array = np.asarray(image, dtype=np.float32) / 255.0
    array = (array - IMAGENET_MEAN) / IMAGENET_STD
    return array.transpose(2, 0, 1)  # HWC -> CHW


async def analyze_note_image(image_bytes: bytes) -> dict:
    """Run NoteAuthNet on a currency note image; returns {feature_name: score} (0-1 each).

    "overall" is the head trained on the genuine/counterfeit label directly (the other
    5 heads share that same weak-supervision label per the training notes) and is what
    classify_verdict() uses for pass/fail; the rest exist for Explainable-AI display.
    """
    try:
        model = _load_note_auth_net()
    except FileNotFoundError:
        return {name: 0.0 for name in FEATURE_NAMES}

    def _infer():
        import numpy as np
        import torch

        array = _preprocess_image(image_bytes)
        tensor = torch.from_numpy(np.ascontiguousarray(array)).float().unsqueeze(0)
        with torch.no_grad():
            return model(tensor).squeeze(0).tolist()

    scores = await asyncio.to_thread(_infer)
    return {name: round(score, 4) for name, score in zip(FEATURE_NAMES, scores)}


# ---------------------------------------------------------------------------
# Counterfeit serial lookup
# ---------------------------------------------------------------------------

async def check_counterfeit_serial(db: AsyncSession, serial_number: str) -> dict | None:
    """Look up a serial number against the known-counterfeit registry."""
    if not serial_number:
        return None
    row = (
        await db.execute(
            text("SELECT * FROM note_verify.counterfeit_serials WHERE serial_number = :serial"),
            {"serial": serial_number},
        )
    ).mappings().first()
    return _to_jsonable(dict(row)) if row else None


async def record_counterfeit_serial(db: AsyncSession, serial_number: str, denomination: int) -> None:
    """Upsert a newly-detected counterfeit serial into the registry."""
    await db.execute(
        text(
            """
            INSERT INTO note_verify.counterfeit_serials (serial_number, denomination, source)
            VALUES (:serial, :denomination, 'detection')
            ON CONFLICT (serial_number) DO UPDATE SET
                detection_count = note_verify.counterfeit_serials.detection_count + 1
            """
        ),
        {"serial": serial_number, "denomination": denomination},
    )


# ---------------------------------------------------------------------------
# Verdict classification
# ---------------------------------------------------------------------------

def classify_verdict(overall_score: float, is_known_counterfeit: bool) -> str:
    """GENUINE >= 0.7, SUSPECT 0.4-0.69, COUNTERFEIT < 0.4 (by overall_score, 0-1 scale).

    A serial-number match against the known-counterfeit registry always wins,
    overriding the image model — a confirmed serial is a stronger signal than a
    single photo's model score.
    """
    if is_known_counterfeit:
        return "COUNTERFEIT"
    if overall_score >= VERDICT_GENUINE_THRESHOLD:
        return "GENUINE"
    if overall_score >= VERDICT_SUSPECT_THRESHOLD:
        return "SUSPECT"
    return "COUNTERFEIT"


# ---------------------------------------------------------------------------
# Verification pipeline — entry point for Srinivas's routers
# ---------------------------------------------------------------------------

async def verify_note(
    db: AsyncSession,
    image_bytes: bytes,
    denomination: int,
    serial_number: str | None = None,
    user_id: UUID | None = None,
    scan_source: str = "mobile",
    device_info: dict | None = None,
    lng: float | None = None,
    lat: float | None = None,
) -> dict:
    """Analyze a currency note image, classify it, and persist the verification record."""
    features = await analyze_note_image(image_bytes)
    overall_score = features["overall"]

    known_counterfeit = await check_counterfeit_serial(db, serial_number) if serial_number else None
    is_known_counterfeit = known_counterfeit is not None

    verdict = classify_verdict(overall_score, is_known_counterfeit)
    confidence = round((1.0 - overall_score if verdict == "COUNTERFEIT" else overall_score) * 100, 2)

    location_clause = "ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)" if lng is not None and lat is not None else "NULL"

    row = (
        await db.execute(
            text(
                f"""
                INSERT INTO note_verify.verifications
                    (user_id, denomination, serial_number, verdict, confidence, feature_analysis,
                     scan_source, device_info, location, is_known_counterfeit)
                VALUES
                    (:user_id, :denomination, :serial_number, :verdict, :confidence, CAST(:features AS JSONB),
                     :scan_source, CAST(:device_info AS JSONB), {location_clause}, :is_known_counterfeit)
                RETURNING id, user_id, denomination, serial_number, verdict, confidence,
                          feature_analysis, scan_source, is_known_counterfeit, created_at
                """
            ),
            {
                "user_id": user_id,
                "denomination": denomination,
                "serial_number": serial_number,
                "verdict": verdict,
                "confidence": confidence,
                "features": json.dumps(features),
                "scan_source": scan_source,
                "device_info": json.dumps(device_info or {}),
                "is_known_counterfeit": is_known_counterfeit,
                "lng": lng,
                "lat": lat,
            },
        )
    ).mappings().first()

    if verdict == "COUNTERFEIT" and serial_number and not is_known_counterfeit:
        await record_counterfeit_serial(db, serial_number, denomination)

    await db.commit()
    return _to_jsonable(dict(row))


# ---------------------------------------------------------------------------
# History + stats
# ---------------------------------------------------------------------------

async def get_verification_history(db: AsyncSession, user_id: UUID, limit: int = 50) -> list[dict]:
    rows = (
        await db.execute(
            text(
                """
                SELECT id, denomination, serial_number, verdict, confidence, scan_source, created_at
                FROM note_verify.verifications
                WHERE user_id = :user_id
                ORDER BY created_at DESC
                LIMIT :limit
                """
            ),
            {"user_id": user_id, "limit": limit},
        )
    ).mappings().all()
    return _to_jsonable([dict(row) for row in rows])


async def get_verification_stats(db: AsyncSession) -> dict:
    row = (
        await db.execute(
            text(
                """
                SELECT
                    COUNT(*) AS total_scans,
                    COUNT(*) FILTER (WHERE verdict = 'GENUINE') AS genuine_count,
                    COUNT(*) FILTER (WHERE verdict = 'SUSPECT') AS suspect_count,
                    COUNT(*) FILTER (WHERE verdict = 'COUNTERFEIT') AS counterfeit_count
                FROM note_verify.verifications
                """
            )
        )
    ).mappings().first()
    return _to_jsonable(dict(row))
