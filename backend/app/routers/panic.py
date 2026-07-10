"""Panic Button API — self-contained per srinivas_mac_core_backend.md §3.1
(no Yashi service logic; Srinivas owns this end-to-end)."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_db

router = APIRouter()


class Location(BaseModel):
    lat: float
    lng: float


class PanicTriggerRequest(BaseModel):
    caller_number: str | None = None
    call_duration_sec: int | None = None
    location: Location | None = None
    device_info: dict | None = None
    emergency_contact_number: str | None = None


@router.post("/trigger")
async def trigger(
    req: PanicTriggerRequest,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    location_clause = "ST_SetSRID(ST_MakePoint(:lng, :lat), 4326)" if req.location else "NULL"
    emergency_notified = req.emergency_contact_number is not None

    row = (
        await db.execute(
            text(
                f"""
                INSERT INTO panic.sos_events
                    (user_id, caller_number, call_duration_sec, location,
                     emergency_contact_notified, emergency_contact_number, device_info)
                VALUES
                    (:user_id, :caller_number, :call_duration_sec, {location_clause},
                     :emergency_notified, :emergency_contact_number, CAST(:device_info AS JSONB))
                RETURNING id, emergency_contact_notified, fraud_report_generated, fraud_report_path, triggered_at
                """
            ),
            {
                "user_id": user["id"],
                "caller_number": req.caller_number,
                "call_duration_sec": req.call_duration_sec,
                "lat": req.location.lat if req.location else None,
                "lng": req.location.lng if req.location else None,
                "emergency_notified": emergency_notified,
                "emergency_contact_number": req.emergency_contact_number,
                "device_info": json.dumps(req.device_info or {}),
            },
        )
    ).mappings().first()
    await db.commit()

    return {
        "report_id": str(row["id"]),
        "emergency_contact_notified": row["emergency_contact_notified"],
        "fraud_report_generated": row["fraud_report_generated"],
        "fraud_report_url": row["fraud_report_path"],
        "triggered_at": row["triggered_at"].isoformat(),
    }
