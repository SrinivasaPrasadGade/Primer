"""Panic Button API — self-contained per srinivas_mac_core_backend.md §3.1
(no Yashi service logic; Srinivas owns this end-to-end)."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_role
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
    # Nothing in this system actually sends a notification yet, so the column stays
    # FALSE. Having a number on file is reported separately as `emergency_contact_on_file`
    # — conflating the two told citizens help was contacted when it never was.
    emergency_notified = False

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
        "emergency_contact_on_file": req.emergency_contact_number is not None,
        "fraud_report_generated": row["fraud_report_generated"],
        "fraud_report_url": row["fraud_report_path"],
        "triggered_at": row["triggered_at"].isoformat(),
    }


@router.get("/events")
async def events(
    limit: int = Query(50, ge=1, le=200),
    user: dict = Depends(require_role("lea_officer")),
    db: AsyncSession = Depends(get_db),
):
    """SOS events, newest first — the officer-facing side of the panic button.

    Without this the mobile SOS wrote to `panic.sos_events` and no one ever read it.
    """
    rows = (
        await db.execute(
            text(
                """
                SELECT s.id, s.caller_number, s.call_duration_sec,
                       ST_Y(s.location) AS lat, ST_X(s.location) AS lng,
                       s.emergency_contact_notified, s.emergency_contact_number,
                       s.fraud_report_generated, s.fraud_report_path,
                       s.device_info, s.triggered_at,
                       u.id AS user_id, u.name AS user_name, u.email AS user_email
                FROM panic.sos_events s
                LEFT JOIN core.users u ON u.id = s.user_id
                ORDER BY s.triggered_at DESC
                LIMIT :limit
                """
            ),
            {"limit": limit},
        )
    ).mappings().all()

    return [
        {
            "id": str(row["id"]),
            "user_id": str(row["user_id"]) if row["user_id"] else None,
            "user_name": row["user_name"],
            "user_email": row["user_email"],
            "caller_number": row["caller_number"],
            "call_duration_sec": row["call_duration_sec"],
            "location": {"lat": row["lat"], "lng": row["lng"]} if row["lat"] is not None else None,
            "emergency_contact_notified": row["emergency_contact_notified"],
            "emergency_contact_number": row["emergency_contact_number"],
            "fraud_report_generated": row["fraud_report_generated"],
            "fraud_report_url": row["fraud_report_path"],
            "device_info": row["device_info"],
            "triggered_at": row["triggered_at"].isoformat(),
        }
        for row in rows
    ]
