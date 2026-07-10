"""Note Verify API layer — wraps app.services.note_verify (Sumanth's NoteAuthNet model
+ Yashi's serial lookup). Srinivas's routers handle upload validation, auth, and
response formatting.
"""

from __future__ import annotations

import base64
import binascii
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.services import note_verify as note_service

router = APIRouter()

MAX_IMAGE_BYTES = 10 * 1024 * 1024  # 10MB — generous for a phone-camera note photo


class NoteVerifyRequest(BaseModel):
    """Matches the TRD §3.3 / mobile contract: base64 image + denomination hint.

    `expo-camera` and the web dashboard both hand back a base64 string (optionally a
    `data:image/...;base64,` data URL), so JSON is the natural transport rather than a
    multipart file upload. denomination defaults to 500 (the most common demo note)
    since the TRD marks it a hint, not required.
    """

    image_base64: str = Field(..., min_length=1)
    denomination: int = 500
    serial_number: str | None = None
    scan_source: str = "mobile"
    lat: float | None = None
    lng: float | None = None


def _decode_image(image_base64: str) -> bytes:
    payload = image_base64.split(",", 1)[-1] if image_base64.startswith("data:") else image_base64
    try:
        return base64.b64decode(payload, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise HTTPException(400, "image_base64 is not valid base64") from exc


@router.post("/verify")
async def verify(
    req: NoteVerifyRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    image_bytes = _decode_image(req.image_base64)
    if not image_bytes:
        raise HTTPException(400, "Decoded image is empty")
    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise HTTPException(413, "Image exceeds the 10MB upload limit")

    return await note_service.verify_note(
        db,
        image_bytes=image_bytes,
        denomination=req.denomination,
        serial_number=req.serial_number,
        user_id=user["id"],
        scan_source=req.scan_source,
        device_info=None,
        lng=req.lng,
        lat=req.lat,
    )


@router.get("/history")
async def history(
    limit: int = 50,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await note_service.get_verification_history(db, UUID(str(user["id"])), limit=limit)


@router.get("/stats")
async def stats(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await note_service.get_verification_stats(db)


@router.get("/serials/{serial}")
async def serial_lookup(
    serial: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await note_service.check_counterfeit_serial(db, serial)
    if not result:
        raise HTTPException(404, "Serial number not found in counterfeit registry")
    return result
