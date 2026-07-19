"""Citizen Shield API layer — wraps app.services.citizen_shield (Yashi's Gemini prompt
engineering + language/risk detection). Srinivas's routers handle request validation,
auth, and response formatting.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.services import citizen_shield as citizen_service
from app.services import scam_sentinel as scam_service

router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: UUID | None = None


@router.post("/chat")
async def chat(
    req: ChatRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if req.session_id is None:
        return await citizen_service.start_chat_session(db, UUID(str(user["id"])), req.message)
    return await citizen_service.send_message(db, req.session_id, req.message)


@router.get("/chat/{session_id}/history")
async def chat_history(
    session_id: UUID,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await citizen_service.get_chat_history(db, session_id)


@router.post("/chat/{session_id}/close")
async def close_chat(
    session_id: UUID,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await citizen_service.close_chat_session(db, session_id)
    return {"session_id": str(session_id), "status": "closed"}


@router.get("/number-check/{phone}")
async def number_check(phone: str, db: AsyncSession = Depends(get_db)):
    """Public number risk check — no auth, per technical_requirements_document.md §3.6."""
    reputation = await scam_service.get_number_reputation(db, phone)
    if not reputation:
        # A miss means "nobody has reported this number to Primer", which is not
        # the same as "this number is safe" — most scam numbers are unreported
        # until after someone has already lost money. `found` lets a client tell
        # the two apart, and the message must not read as an all-clear: this is
        # a public endpoint a citizen may consult mid-call, before deciding
        # whether to trust the caller.
        return {
            "phone": phone,
            "found": False,
            "risk_score": 0,
            "is_blacklisted": False,
            "message": (
                "No one has reported this number to Primer. That is not a safety "
                "guarantee — an unreported number can still be a scam. Stay cautious."
            ),
        }
    return {"found": True, **scam_service._to_jsonable(reputation)}
