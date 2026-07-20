"""Adaptive Fraud KB API — exposes app.services.knowledge_base.

The service, its migration and its seed data all predate this router; until it
existed the whole feature was unreachable from any client.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_role
from app.database import get_db
from app.services import knowledge_base as kb_service

router = APIRouter()


class MatchRequest(BaseModel):
    text: str = Field(..., min_length=1)
    top_k: int = Field(5, ge=1, le=20)


class AddPatternRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    scam_type: str = Field(..., min_length=1, max_length=50)
    language: str = "en"
    key_indicators: list[str] | None = None


@router.get("/patterns")
async def list_patterns(
    scam_type: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await kb_service.list_patterns(db, scam_type=scam_type, limit=limit)


@router.post("/match")
async def match(
    req: MatchRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Match free text against the pattern library, recording the hit.

    Takes the text from the caller rather than reading it off a scam session:
    scam_sessions has no transcript column, so there is no stored text to match.
    """
    return await kb_service.match_and_record_pattern(db, req.text, top_k=req.top_k)


@router.post("/patterns")
async def add_pattern(
    req: AddPatternRequest,
    user: dict = Depends(require_role("lea_officer")),
    db: AsyncSession = Depends(get_db),
):
    return await kb_service.add_pattern(
        db,
        title=req.title,
        description=req.description,
        scam_type=req.scam_type,
        labeled_by=user["id"],
        language=req.language,
        key_indicators=req.key_indicators,
    )


@router.post("/patterns/{pattern_id}/verify")
async def verify_pattern(
    pattern_id: UUID,
    user: dict = Depends(require_role("lea_officer")),
    db: AsyncSession = Depends(get_db),
):
    result = await kb_service.verify_pattern(db, pattern_id)
    if not result:
        raise HTTPException(404, "Pattern not found")
    return result


@router.post("/backfill-embeddings")
async def backfill_embeddings(
    limit: int = Query(200, ge=1, le=1000),
    user: dict = Depends(require_role("lea_officer")),
    db: AsyncSession = Depends(get_db),
):
    """Embed any patterns missing one. The seed data ships without embeddings, so
    this must run once before /match returns anything."""
    updated = await kb_service.backfill_embeddings(db, limit=limit)
    return {"patterns_embedded": updated}
