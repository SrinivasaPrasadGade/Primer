"""Geo Intel: PostGIS heatmap aggregation, incident pins, hotspot prediction integration.

Yashi's logic layer — Srinivas's routers call these functions and return their JSON-ready
dicts/lists directly; no ORM models, raw SQL via SQLAlchemy Core (matches correlation.py).
"""

from __future__ import annotations

import json
import logging
from datetime import date
from functools import lru_cache
from pathlib import Path

import numpy as np
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

ML_MODELS_DIR = Path(__file__).resolve().parent.parent / "ml" / "models"
MODEL_VERSION = "hotspot_predictor_v1"

# The MVP schema has no dedicated population/ATM-density dataset, but the trained model
# was fit expecting those two features — fall back to fixed city-average constants rather
# than standing up a separate geospatial ingestion pipeline for a hackathon demo.
DEFAULT_POPULATION_DENSITY = 20000.0  # people / sq km, roughly Mumbai suburban average
DEFAULT_BANK_ATM_DENSITY = 15.0  # ATMs / sq km


def _to_jsonable(value):
    """Round-trip UUID/datetime/Decimal through JSON so they're plain str/float."""
    return json.loads(json.dumps(value, default=str))


# ---------------------------------------------------------------------------
# Heatmap + incident pins
# ---------------------------------------------------------------------------

async def get_heatmap_data(
    db: AsyncSession, bounds: dict, crime_type: str | None = None, days: int = 7
) -> list[dict]:
    """Aggregate incidents into ~0.01-degree grid cells for heatmap visualisation.

    Groups by the snapped grid point (not the raw location) so lng/lat in the SELECT
    match the GROUP BY — grouping by ST_SnapToGrid while selecting the ungrouped raw
    location, as a naive first draft might, is invalid SQL under Postgres's aggregate rules.
    """
    query = text(
        """
        SELECT
            ST_X(ST_SnapToGrid(location, 0.01)) AS lng,
            ST_Y(ST_SnapToGrid(location, 0.01)) AS lat,
            COUNT(*) AS intensity,
            crime_type
        FROM geo_intel.incidents
        WHERE reported_at >= NOW() - (:days * INTERVAL '1 day')
        AND ST_Within(location, ST_MakeEnvelope(:west, :south, :east, :north, 4326))
        AND ((:crime_type)::varchar IS NULL OR crime_type = :crime_type)
        GROUP BY ST_SnapToGrid(location, 0.01), crime_type
        ORDER BY intensity DESC
        """
    )
    rows = (await db.execute(query, {**bounds, "days": days, "crime_type": crime_type})).mappings().all()
    return _to_jsonable([dict(row) for row in rows])


async def get_incident_pins(
    db: AsyncSession, bounds: dict, crime_type: str | None = None, limit: int = 500
) -> list[dict]:
    """Get individual incident pins for map display."""
    query = text(
        """
        SELECT id, crime_type, title, description,
               ST_X(location) AS lng, ST_Y(location) AS lat,
               severity, estimated_loss, reported_at
        FROM geo_intel.incidents
        WHERE ST_Within(location, ST_MakeEnvelope(:west, :south, :east, :north, 4326))
        AND ((:crime_type)::varchar IS NULL OR crime_type = :crime_type)
        ORDER BY reported_at DESC
        LIMIT :limit
        """
    )
    rows = (await db.execute(query, {**bounds, "crime_type": crime_type, "limit": limit})).mappings().all()
    return _to_jsonable([dict(row) for row in rows])


# ---------------------------------------------------------------------------
# Hotspot prediction — trained Random Forest classifier
# ---------------------------------------------------------------------------

HOTSPOT_FEATURES = [
    "latitude", "longitude", "crime_count_7d", "crime_count_30d",
    "population_density", "bank_atm_density", "day_of_week", "month",
    "avg_loss_amount_area",
]


@lru_cache(maxsize=1)
def _load_hotspot_model():
    import joblib

    return joblib.load(ML_MODELS_DIR / "hotspot_predictor.joblib")


def _grid_points(bounds: dict, cell_km: float) -> list[tuple[float, float]]:
    """Generate candidate (lat, lng) grid points across bounds at ~cell_km spacing."""
    lat_step = cell_km / 111.0  # ~111 km per degree of latitude
    mid_lat = (bounds["south"] + bounds["north"]) / 2
    lng_step = cell_km / (111.0 * max(0.1, np.cos(np.radians(mid_lat))))

    points = []
    lat = bounds["south"]
    while lat <= bounds["north"]:
        lng = bounds["west"]
        while lng <= bounds["east"]:
            points.append((lat, lng))
            lng += lng_step
        lat += lat_step
    return points


async def _crime_counts_near(db: AsyncSession, lat: float, lng: float, radius_km: float) -> dict:
    """Count incidents within radius_km of (lat, lng) over the last 7/30 days, plus avg loss."""
    query = text(
        """
        SELECT
            COUNT(*) FILTER (WHERE reported_at >= NOW() - INTERVAL '7 days') AS crime_count_7d,
            COUNT(*) FILTER (WHERE reported_at >= NOW() - INTERVAL '30 days') AS crime_count_30d,
            COALESCE(AVG(estimated_loss), 0) AS avg_loss_amount_area
        FROM geo_intel.incidents
        WHERE ST_DWithin(location::geography, ST_MakePoint(:lng, :lat)::geography, :radius_m)
        """
    )
    row = (
        await db.execute(query, {"lat": lat, "lng": lng, "radius_m": radius_km * 1000})
    ).mappings().first()
    return dict(row) if row else {"crime_count_7d": 0, "crime_count_30d": 0, "avg_loss_amount_area": 0}


async def generate_hotspot_predictions(
    db: AsyncSession,
    bounds: dict,
    crime_type: str | None = None,
    grid_km: float = 2.0,
    risk_threshold: int = 50,
) -> list[dict]:
    """Score a grid of candidate points across bounds with the trained hotspot model,
    persist predictions scoring at/above risk_threshold, and return them.

    Per-point crime-count queries run sequentially — a single AsyncSession/connection
    isn't safe to fan out concurrently, and at demo scale (a city bounding box, 1-2km
    grid) this is a few dozen round trips, not thousands.
    """
    model = _load_hotspot_model()
    today = date.today()
    points = _grid_points(bounds, grid_km)
    if not points:
        return []

    features = []
    for lat, lng in points:
        counts = await _crime_counts_near(db, lat, lng, radius_km=grid_km)
        features.append(
            [
                lat, lng,
                counts["crime_count_7d"], counts["crime_count_30d"],
                DEFAULT_POPULATION_DENSITY, DEFAULT_BANK_ATM_DENSITY,
                today.weekday(), today.month,
                float(counts["avg_loss_amount_area"]),
            ]
        )

    risk_scores = model.predict_proba(np.array(features, dtype=np.float32))[:, 1] * 100

    predictions = []
    for (lat, lng), risk_score in zip(points, risk_scores):
        if risk_score < risk_threshold:
            continue
        row = (
            await db.execute(
                text(
                    """
                    INSERT INTO geo_intel.predictions
                        (prediction_date, crime_type, center_point, radius_km, risk_score, model_version)
                    VALUES (:pdate, :crime_type, ST_SetSRID(ST_MakePoint(:lng, :lat), 4326),
                            :radius_km, :risk_score, :model_version)
                    RETURNING id, prediction_date, crime_type, ST_X(center_point) AS lng,
                              ST_Y(center_point) AS lat, radius_km, risk_score, model_version
                    """
                ),
                {
                    "pdate": today,
                    "crime_type": crime_type,
                    "lng": lng,
                    "lat": lat,
                    "radius_km": grid_km / 2,
                    "risk_score": round(float(risk_score)),
                    "model_version": MODEL_VERSION,
                },
            )
        ).mappings().first()
        predictions.append(dict(row))

    if predictions:
        await db.commit()
    return _to_jsonable(predictions)


async def get_stored_predictions(
    db: AsyncSession, bounds: dict, prediction_date: date | None = None
) -> list[dict]:
    """Fetch already-generated hotspot predictions within bounds (GET /geo/predictions)."""
    query = text(
        """
        SELECT id, prediction_date, crime_type,
               ST_X(center_point) AS lng, ST_Y(center_point) AS lat,
               radius_km, risk_score, model_version
        FROM geo_intel.predictions
        WHERE ST_Within(center_point, ST_MakeEnvelope(:west, :south, :east, :north, 4326))
        AND ((:prediction_date)::date IS NULL OR prediction_date = :prediction_date)
        ORDER BY risk_score DESC
        """
    )
    rows = (
        await db.execute(query, {**bounds, "prediction_date": prediction_date})
    ).mappings().all()
    return _to_jsonable([dict(row) for row in rows])
