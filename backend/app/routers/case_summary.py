"""Case Summarizer API layer — wraps app.services.case_summary (Yashi's evidence
extraction + Gemini-powered summarization). Srinivas's routers handle request
validation, auth, and response formatting.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import require_role
from app.database import get_db
from app.services import case_summary as case_service

router = APIRouter()

VALID_ENTITY_TYPES = (
    "phone_number", "bank_account", "upi_id", "person", "device", "ip_address", "complaint",
)


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
