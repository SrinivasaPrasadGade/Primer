"""Pre-Answer Call Screening API — self-contained per srinivas_mac_core_backend.md §3.1
(uses scam_sentinel.number_reputation directly, no dedicated Yashi service module)."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.services import scam_sentinel as scam_service

router = APIRouter()

_HIGH_RISK_THRESHOLD = 70
_MEDIUM_RISK_THRESHOLD = 30


def _risk_level(risk_score: int) -> str:
    if risk_score >= _HIGH_RISK_THRESHOLD:
        return "high"
    if risk_score >= _MEDIUM_RISK_THRESHOLD:
        return "medium"
    return "low"


def _recommendation(risk_level: str, is_blacklisted: bool) -> str:
    if is_blacklisted or risk_level == "high":
        return "block"
    if risk_level == "medium":
        return "caution"
    return "allow"


@router.get("/number/{phone}")
async def screen_number(
    phone: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    reputation = await scam_service.get_number_reputation(db, phone)
    if not reputation:
        return {"risk_level": "low", "risk_score": 0, "flags": [], "recommendation": "allow"}

    risk_score = reputation["risk_score"]
    risk_level = _risk_level(risk_score)
    flags = []
    if reputation.get("is_blacklisted"):
        flags.append("blacklisted")
    if reputation.get("primary_scam_type"):
        flags.append(reputation["primary_scam_type"])

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "flags": flags,
        "recommendation": _recommendation(risk_level, bool(reputation.get("is_blacklisted"))),
    }
