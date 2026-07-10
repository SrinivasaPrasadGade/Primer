"""Note Verify API layer — wraps app.services.note_verify (Sumanth's NoteAuthNet model
+ Yashi's serial lookup). Srinivas's routers handle upload validation, auth, and
response formatting.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.services import note_verify as note_service

router = APIRouter()

MAX_IMAGE_BYTES = 10 * 1024 * 1024  # 10MB — generous for a phone-camera note photo


@router.post("/verify")
async def verify(
    denomination: int = Form(...),
    serial_number: str | None = Form(None),
    scan_source: str = Form("mobile"),
    lng: float | None = Form(None),
    lat: float | None = Form(None),
    image: UploadFile = File(...),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(400, "Uploaded image is empty")
    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise HTTPException(413, "Image exceeds the 10MB upload limit")

    return await note_service.verify_note(
        db,
        image_bytes=image_bytes,
        denomination=denomination,
        serial_number=serial_number,
        user_id=user["id"],
        scan_source=scan_source,
        device_info=None,
        lng=lng,
        lat=lat,
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
