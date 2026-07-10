"""Geo Intel API layer — wraps app.services.geo_intel (Yashi's PostGIS aggregation +
Sumanth's hotspot-predictor model). Srinivas's routers handle bounds validation, auth,
and response formatting.

Bounds are passed as a single `bounds` query param ("west,south,east,north"), matching
TRD §3.5 and Nivedita's frontend client (Mapbox `map.getBounds()` flattened) rather than
four separate params.
"""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, require_role
from app.database import get_db
from app.services import geo_intel as geo_service

router = APIRouter()


def parse_bounds(bounds: str = Query(..., description="'west,south,east,north' (e.g. 72.77,18.89,72.99,19.27)")) -> dict:
    """Parse the shared bounds query param into the dict shape the service expects."""
    parts = bounds.split(",")
    if len(parts) != 4:
        raise HTTPException(400, "bounds must be 'west,south,east,north'")
    try:
        west, south, east, north = (float(p) for p in parts)
    except ValueError as exc:
        raise HTTPException(400, "bounds values must be numbers") from exc
    return {"west": west, "south": south, "east": east, "north": north}


@router.get("/heatmap")
async def heatmap(
    bounds: dict = Depends(parse_bounds),
    crime_type: str | None = Query(None, alias="type"),
    days: int = Query(7, ge=1, le=90),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await geo_service.get_heatmap_data(db, bounds, crime_type=crime_type, days=days)


@router.get("/incidents")
async def incidents(
    bounds: dict = Depends(parse_bounds),
    crime_type: str | None = Query(None, alias="type"),
    limit: int = Query(500, ge=1, le=2000),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await geo_service.get_incident_pins(db, bounds, crime_type=crime_type, limit=limit)


@router.get("/predictions")
async def predictions(
    bounds: dict = Depends(parse_bounds),
    prediction_date: date | None = Query(None),
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await geo_service.get_stored_predictions(db, bounds, prediction_date=prediction_date)


@router.post("/predictions/generate")
async def generate_predictions(
    bounds: dict = Depends(parse_bounds),
    crime_type: str | None = Query(None, alias="type"),
    grid_km: float = Query(2.0, gt=0, le=20),
    risk_threshold: int = Query(50, ge=0, le=100),
    user: dict = Depends(require_role("lea_officer")),
    db: AsyncSession = Depends(get_db),
):
    return await geo_service.generate_hotspot_predictions(
        db,
        bounds,
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
