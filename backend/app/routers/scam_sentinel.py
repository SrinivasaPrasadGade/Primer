"""Scam Sentinel API layer — wraps app.services.scam_sentinel (Yashi's signal scoring
and number-reputation logic). Srinivas's routers handle request validation, auth, and
response formatting; they never compute signal scores themselves.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_role
from app.database import get_db
from app.services import scam_sentinel as scam_service

router = APIRouter()

_LIST_COLUMNS = """
    id, caller_number, callee_number, call_start, call_end, call_duration_sec,
    alert_level, overall_confidence, scam_type, scam_phase, status, created_at
"""


class AcknowledgeResponse(BaseModel):
    id: str
    status: str
    acknowledged_by: str
    acknowledged_at: str | None = None


class FlagNumberRequest(BaseModel):
    alert_level: str = Field(..., pattern="^(RED|AMBER|YELLOW)$")


# ---------------------------------------------------------------------------
# Live feed — connected clients + broadcast helper, per srinivas_mac_core_backend.md §5
# ---------------------------------------------------------------------------

_connected_clients: list[WebSocket] = []


async def broadcast_new_session(session_data: dict) -> None:
    for client in list(_connected_clients):
        try:
            await client.send_json(session_data)
        except Exception:
            _connected_clients.remove(client)


@router.websocket("/ws/live")
async def scam_live_feed(websocket: WebSocket):
    await websocket.accept()
    _connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep-alive; client doesn't need to send anything meaningful
    except WebSocketDisconnect:
        if websocket in _connected_clients:
            _connected_clients.remove(websocket)


# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------

@router.get("/sessions")
async def list_sessions(
    alert_level: str | None = Query(None, pattern="^(RED|AMBER|YELLOW|NONE)$"),
    status: str | None = Query(None, pattern="^(active|classified|acknowledged|investigating|closed)$"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    user: dict = Depends(require_role("lea_officer", "bank_manager")),
    db: AsyncSession = Depends(get_db),
):
    query = text(
        f"""
        SELECT {_LIST_COLUMNS} FROM scam_sentinel.scam_sessions
        WHERE ((:alert_level)::varchar IS NULL OR alert_level = :alert_level)
        AND ((:status)::varchar IS NULL OR status = :status)
        ORDER BY created_at DESC
        LIMIT :limit OFFSET :offset
        """
    )
    rows = (
        await db.execute(query, {"alert_level": alert_level, "status": status, "limit": limit, "offset": offset})
    ).mappings().all()
    return scam_service._to_jsonable([dict(row) for row in rows])


@router.get("/sessions/{session_id}")
async def get_session(
    session_id: UUID,
    user: dict = Depends(require_role("lea_officer", "bank_manager")),
    db: AsyncSession = Depends(get_db),
):
    session = await scam_service.get_session_detail(db, session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    return session


@router.post("/sessions/{session_id}/classify")
async def classify_session(
    session_id: UUID,
    user: dict = Depends(require_role("lea_officer", "bank_manager")),
    db: AsyncSession = Depends(get_db),
):
    """Run the signal-scoring pipeline for a session (Yashi's process_scam_session
    entry point) and broadcast the result to any connected live-feed clients."""
    try:
        result = await scam_service.process_scam_session(db, session_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    await broadcast_new_session(result)
    return result


@router.post("/sessions/{session_id}/acknowledge", response_model=AcknowledgeResponse)
async def acknowledge_session(
    session_id: UUID,
    user: dict = Depends(require_role("lea_officer", "bank_manager")),
    db: AsyncSession = Depends(get_db),
):
    row = (
        await db.execute(
            text(
                """
                UPDATE scam_sentinel.scam_sessions
                SET status = 'acknowledged', acknowledged_by = :user_id, acknowledged_at = NOW(), updated_at = NOW()
                WHERE id = :session_id
                RETURNING id, status, acknowledged_by, acknowledged_at
                """
            ),
            {"user_id": user["id"], "session_id": session_id},
        )
    ).mappings().first()
    if not row:
        raise HTTPException(404, "Session not found")
    await db.commit()
    return AcknowledgeResponse(
        id=str(row["id"]),
        status=row["status"],
        acknowledged_by=str(row["acknowledged_by"]),
        acknowledged_at=row["acknowledged_at"].isoformat() if row["acknowledged_at"] else None,
    )


# ---------------------------------------------------------------------------
# Number reputation
# ---------------------------------------------------------------------------

@router.get("/numbers/{phone}")
async def get_number(
    phone: str,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    reputation = await scam_service.get_number_reputation(db, phone)
    if not reputation:
        raise HTTPException(404, "No reputation data for this number")
    return scam_service._to_jsonable(reputation)


@router.post("/numbers/{phone}/flag")
async def flag_number(
    phone: str,
    req: FlagNumberRequest,
    user: dict = Depends(require_role("lea_officer", "bank_manager")),
    db: AsyncSession = Depends(get_db),
):
    result = await scam_service.update_number_reputation(db, phone, req.alert_level)
    return scam_service._to_jsonable(result)


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

@router.get("/stats")
async def get_stats(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    row = (
        await db.execute(
            text(
                """
                SELECT
                    COUNT(*) AS total_sessions,
                    COUNT(*) FILTER (WHERE alert_level = 'RED') AS red_count,
                    COUNT(*) FILTER (WHERE alert_level = 'AMBER') AS amber_count,
                    COUNT(*) FILTER (WHERE alert_level = 'YELLOW') AS yellow_count,
                    COUNT(*) FILTER (WHERE status = 'active') AS active_count,
                    COALESCE(AVG(overall_confidence), 0) AS avg_confidence
                FROM scam_sentinel.scam_sessions
                """
            )
        )
    ).mappings().first()
    return scam_service._to_jsonable(dict(row))
