"""Unit tests for app.services.geo_intel — mocked AsyncSession + mocked model, no live Postgres needed."""

from datetime import date
from unittest.mock import AsyncMock

import numpy as np
import pytest

from app.services import geo_intel as svc


class FakeResult:
    def __init__(self, row=None, rows=None):
        self._row = row
        self._rows = rows or []

    def mappings(self):
        return self

    def first(self):
        return self._row

    def all(self):
        return self._rows


BOUNDS = {"west": 72.8, "south": 19.0, "east": 72.9, "north": 19.1}


# ---------------------------------------------------------------------------
# Heatmap + pins
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_heatmap_data():
    rows = [{"lng": 72.85, "lat": 19.05, "intensity": 12, "crime_type": "upi_fraud"}]
    db = AsyncMock()
    db.execute.return_value = FakeResult(rows=rows)

    result = await svc.get_heatmap_data(db, BOUNDS, crime_type="upi_fraud", days=7)

    assert result == rows
    params = db.execute.call_args[0][1]
    assert params["crime_type"] == "upi_fraud"
    assert params["days"] == 7
    assert params["west"] == 72.8


@pytest.mark.asyncio
async def test_get_heatmap_data_no_filter():
    db = AsyncMock()
    db.execute.return_value = FakeResult(rows=[])
    result = await svc.get_heatmap_data(db, BOUNDS)
    assert result == []
    assert db.execute.call_args[0][1]["crime_type"] is None


@pytest.mark.asyncio
async def test_get_incident_pins():
    rows = [
        {
            "id": "abc", "crime_type": "phishing", "title": "t", "description": "d",
            "lng": 72.85, "lat": 19.05, "severity": "high", "estimated_loss": 10000.0,
            "reported_at": None,
        }
    ]
    db = AsyncMock()
    db.execute.return_value = FakeResult(rows=rows)

    result = await svc.get_incident_pins(db, BOUNDS, limit=100)

    assert len(result) == 1
    assert db.execute.call_args[0][1]["limit"] == 100


# ---------------------------------------------------------------------------
# Grid generation
# ---------------------------------------------------------------------------

def test_grid_points_covers_bounds():
    points = svc._grid_points(BOUNDS, cell_km=2.0)
    assert len(points) > 0
    for lat, lng in points:
        assert BOUNDS["south"] <= lat <= BOUNDS["north"] + 1e-6
        assert BOUNDS["west"] <= lng <= BOUNDS["east"] + 1e-6


def test_grid_points_finer_grid_yields_more_points():
    coarse = svc._grid_points(BOUNDS, cell_km=5.0)
    fine = svc._grid_points(BOUNDS, cell_km=1.0)
    assert len(fine) > len(coarse)


# ---------------------------------------------------------------------------
# generate_hotspot_predictions — mocked model + mocked DB
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_generate_hotspot_predictions_filters_below_threshold(monkeypatch):
    class FakeModel:
        def predict_proba(self, X):
            # First point scores high (kept), rest score low (filtered out)
            n = len(X)
            probs = np.zeros((n, 2))
            probs[0] = [0.2, 0.8]
            probs[1:] = [0.9, 0.1]
            return probs

    monkeypatch.setattr(svc, "_load_hotspot_model", lambda: FakeModel())
    monkeypatch.setattr(
        svc, "_crime_counts_for_points",
        AsyncMock(side_effect=lambda db, points, radius_km: [
            {"crime_count_7d": 5, "crime_count_30d": 20, "avg_loss_amount_area": 30000.0} for _ in points
        ]),
    )

    db = AsyncMock()
    db.execute.return_value = FakeResult(
        row={
            "id": "pred1", "prediction_date": date.today(), "crime_type": "upi_fraud",
            "lng": 72.85, "lat": 19.05, "radius_km": 1.0, "risk_score": 80, "model_version": "hotspot_predictor_v1",
        }
    )

    result = await svc.generate_hotspot_predictions(db, BOUNDS, crime_type="upi_fraud", grid_km=5.0, risk_threshold=50)

    # Only the single high-scoring point should have triggered an INSERT
    assert len(result) == 1
    assert result[0]["risk_score"] == 80
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_generate_hotspot_predictions_none_above_threshold(monkeypatch):
    class FakeModel:
        def predict_proba(self, X):
            n = len(X)
            probs = np.tile([0.9, 0.1], (n, 1))
            return probs

    monkeypatch.setattr(svc, "_load_hotspot_model", lambda: FakeModel())
    monkeypatch.setattr(
        svc, "_crime_counts_for_points",
        AsyncMock(side_effect=lambda db, points, radius_km: [
            {"crime_count_7d": 0, "crime_count_30d": 0, "avg_loss_amount_area": 0} for _ in points
        ]),
    )

    db = AsyncMock()
    result = await svc.generate_hotspot_predictions(db, BOUNDS, grid_km=5.0, risk_threshold=50)

    assert result == []

    # _crime_counts_for_points is mocked out, so the only statements reaching the DB
    # here are the clear-then-insert pair. Nothing cleared the threshold, so the
    # DELETE runs and no INSERT follows it.
    assert db.execute.await_count == 1
    statement = str(db.execute.await_args_list[0].args[0])
    assert "DELETE FROM geo_intel.predictions" in statement

    # ...and it must still commit. The DELETE shares this transaction, so
    # skipping the commit on an empty result would roll back the clear and leave
    # the previous run's now-stale hotspots on the map.
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_stored_predictions():
    rows = [
        {
            "id": "p1", "prediction_date": date.today(), "crime_type": "upi_fraud",
            "lng": 72.85, "lat": 19.05, "radius_km": 1.0, "risk_score": 70, "model_version": "v1",
        }
    ]
    db = AsyncMock()
    db.execute.return_value = FakeResult(rows=rows)

    result = await svc.get_stored_predictions(db, BOUNDS)

    assert len(result) == 1
    assert result[0]["risk_score"] == 70


# ---------------------------------------------------------------------------
# _crime_counts_for_points — batched grid lookup
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_crime_counts_for_points_is_one_query_and_keeps_order():
    points = [(19.0, 72.8), (19.1, 72.9), (19.2, 73.0)]
    db = AsyncMock()
    db.execute.return_value = FakeResult(rows=[
        {"idx": 1, "crime_count_7d": 5, "crime_count_30d": 9, "avg_loss_amount_area": 100},
        {"idx": 2, "crime_count_7d": 0, "crime_count_30d": 1, "avg_loss_amount_area": 0},
        {"idx": 3, "crime_count_7d": 7, "crime_count_30d": 8, "avg_loss_amount_area": 250},
    ])

    result = await svc._crime_counts_for_points(db, points, radius_km=2.0)

    # One statement for the whole grid, not one per point.
    assert db.execute.await_count == 1
    assert [r["crime_count_7d"] for r in result] == [5, 0, 7]

    params = db.execute.await_args.args[1]
    assert params["lats"] == [19.0, 19.1, 19.2]
    assert params["lngs"] == [72.8, 72.9, 73.0]
    assert params["radius_m"] == 2000.0


@pytest.mark.asyncio
async def test_crime_counts_for_points_fills_gaps_without_shifting():
    """A point the query returns no row for must yield zeros in its own slot."""
    points = [(19.0, 72.8), (19.1, 72.9), (19.2, 73.0)]
    db = AsyncMock()
    # Middle point absent from the result set.
    db.execute.return_value = FakeResult(rows=[
        {"idx": 1, "crime_count_7d": 5, "crime_count_30d": 9, "avg_loss_amount_area": 100},
        {"idx": 3, "crime_count_7d": 7, "crime_count_30d": 8, "avg_loss_amount_area": 250},
    ])

    result = await svc._crime_counts_for_points(db, points, radius_km=2.0)

    assert len(result) == 3
    assert [r["crime_count_7d"] for r in result] == [5, 0, 7]


@pytest.mark.asyncio
async def test_crime_counts_for_points_empty_grid_skips_the_query():
    db = AsyncMock()
    assert await svc._crime_counts_for_points(db, [], radius_km=2.0) == []
    db.execute.assert_not_awaited()
