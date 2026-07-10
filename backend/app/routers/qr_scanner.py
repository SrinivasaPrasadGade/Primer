"""QR Scanner API layer — wraps app.services.qr_scanner (Yashi's UPI/URL risk
assessment). Srinivas's routers handle request validation, auth, and response
formatting.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.services import qr_scanner as qr_service

router = APIRouter()


class QrScanRequest(BaseModel):
    qr_content: str = Field(..., min_length=1, max_length=2000)


@router.post("/scan")
async def scan(
    req: QrScanRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await qr_service.scan_qr_code(db, req.qr_content, user_id=user["id"])
