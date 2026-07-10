"""Geo Intel API layer — wraps app.services.geo_intel (Yashi's PostGIS aggregation +
Sumanth's hotspot-predictor model). Srinivas's routers handle bounds validation, auth,
and response formatting.
"""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_role
from app.database import get_db
from app.services import geo_intel as geo_service

router = APIRouter()


def _bounds(west: float, south: float, east: float, north: float) -> dict:
    return {"west": west, "south": south, "east": east, "north": north}


@router.get("/heatmap")
async def heatmap(
    west: float = Query(...),
    south: float = Query(...),
    east: float = Query(...),
    north: float = Query(...),
    crime_type: str | None = Query(None),
    days: int = Query(7, ge=1, le=90),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await geo_service.get_heatmap_data(db, _bounds(west, south, east, north), crime_type=crime_type, days=days)


@router.get("/incidents")
async def incidents(
    west: float = Query(...),
    south: float = Query(...),
    east: float = Query(...),
    north: float = Query(...),
    crime_type: str | None = Query(None),
    limit: int = Query(500, ge=1, le=2000),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await geo_service.get_incident_pins(
        db, _bounds(west, south, east, north), crime_type=crime_type, limit=limit
    )


@router.get("/predictions")
async def predictions(
    west: float = Query(...),
    south: float = Query(...),
    east: float = Query(...),
    north: float = Query(...),
    prediction_date: date | None = Query(None),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await geo_service.get_stored_predictions(
        db, _bounds(west, south, east, north), prediction_date=prediction_date
    )


@router.post("/predictions/generate")
async def generate_predictions(
    west: float = Query(...),
    south: float = Query(...),
    east: float = Query(...),
    north: float = Query(...),
    crime_type: str | None = Query(None),
    grid_km: float = Query(2.0, gt=0, le=20),
    risk_threshold: int = Query(50, ge=0, le=100),
    user: dict = Depends(require_role("lea_officer")),
    db: AsyncSession = Depends(get_db),
):
    return await geo_service.generate_hotspot_predictions(
        db,
        _bounds(west, south, east, north),
        crime_type=crime_type,
        grid_km=grid_km,
        risk_threshold=risk_threshold,
    )


@router.get("/stats")
async def stats(
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    rows = (
        await db.execute(
            text(
                """
                SELECT crime_type, state, district, COUNT(*) AS incident_count,
                       COALESCE(SUM(estimated_loss), 0) AS total_loss
                FROM geo_intel.incidents
                GROUP BY crime_type, state, district
                ORDER BY incident_count DESC
                LIMIT 100
                """
            )
        )
    ).mappings().all()
    return geo_service._to_jsonable([dict(row) for row in rows])
