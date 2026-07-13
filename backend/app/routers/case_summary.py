"""Case Summarizer API layer — wraps app.services.case_summary (Yashi's evidence
extraction + Gemini-powered summarization). Srinivas's routers handle request
validation, auth, and response formatting.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import require_role
from app.database import get_db
from app.services import case_summary as case_service

router = APIRouter()

VALID_ENTITY_TYPES = (
    "phone_number", "bank_account", "upi_id", "person", "device", "ip_address", "complaint",
)

MAX_CASE_FILE_BYTES = 1 * 1024 * 1024  # 1 MB
ALLOWED_SUFFIXES = (".txt", ".json", ".csv", ".log")


class SummarizeRequest(BaseModel):
    entity_type: str = Field(..., description=f"One of {VALID_ENTITY_TYPES}")
    entity_value: str
    investigation_id: UUID | None = None


@router.post("/summarize")
async def summarize(
    req: SummarizeRequest,
    user: dict = Depends(require_role("lea_officer", "bank_manager")),
    db: AsyncSession = Depends(get_db),
):
    return await case_service.summarize_and_store(
        db,
        entity_type=req.entity_type,
        entity_value=req.entity_value,
        generated_by=UUID(str(user["id"])),
        investigation_id=req.investigation_id,
    )


@router.post("/summarize-file")
async def summarize_file(
    file: UploadFile = File(...),
    investigation_id: UUID | None = Form(None),
    user: dict = Depends(require_role("lea_officer", "bank_manager")),
    db: AsyncSession = Depends(get_db),
):
    """Summarise an uploaded case/complaint file's text directly (no entity lookup).

    Returns the same CaseSummary shape as /summarize, with source_evidence recording
    "upload:<filename>".
    """
    if not file.filename or not file.filename.lower().endswith(ALLOWED_SUFFIXES):
        raise HTTPException(415, f"Only {', '.join(ALLOWED_SUFFIXES)} files are supported")

    raw = await file.read()
    if len(raw) > MAX_CASE_FILE_BYTES:
        raise HTTPException(413, "Case file exceeds the 1MB limit")

    try:
        evidence_text = raw.decode("utf-8").strip()
    except UnicodeDecodeError:
        raise HTTPException(400, "File is not valid UTF-8 text")
    if not evidence_text:
        raise HTTPException(400, "File is empty")

    return await case_service.summarize_text_and_store(
        db,
        evidence_text=evidence_text,
        source_label=f"upload:{file.filename}",
        generated_by=UUID(str(user["id"])),
        investigation_id=investigation_id,
    )
