"""Populate geo_intel.predictions by running the real hotspot model once.

`geo_intel.predictions` is written by exactly one code path — POST /geo/predictions/
generate — and nothing invokes it automatically, so the table stays empty and the
Geo Intel map reports 0 predicted hotspots on a fresh database.

This runs that same code path over the demo bounding box after seeding, so the map
has real, correctly-versioned model output on first load. It deliberately does NOT
insert hand-written rows: a fabricated prediction stamped with a real model_version
is indistinguishable from genuine inference, which is exactly the failure this
module is supposed to avoid.

Run after loading 01_seed.sql:

    python -m scripts.bootstrap_predictions

Safe to re-run — generate_hotspot_predictions clears the same day's predictions for
the requested bounds before inserting.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from sqlalchemy import text

from app.database import async_session, engine
from app.services import geo_intel as geo_service

logger = logging.getLogger("bootstrap_predictions")

# Greater Mumbai — matches DEFAULT_BOUNDS in frontend/dashboard/src/app/geo/page.tsx,
# so the seeded forecast covers the viewport the map actually opens on.
DEFAULT_BOUNDS = {"west": 72.77, "south": 18.89, "east": 72.99, "north": 19.27}


async def _should_run(db) -> bool:
    """True when there is incident data to forecast from but no forecast yet.

    Guards the --if-needed path used at container start, which runs before the
    manual seed load. On an unseeded database every grid point scores near zero,
    so running then would store nothing and leave the map empty anyway; skipping
    keeps the log honest about why. Once seeded, the next start populates it.
    """
    incidents = (await db.execute(text("SELECT COUNT(*) FROM geo_intel.incidents"))).scalar() or 0
    if incidents == 0:
        logger.info("No incidents in geo_intel.incidents yet — skipping. Load 01_seed.sql first.")
        return False

    predictions = (await db.execute(text("SELECT COUNT(*) FROM geo_intel.predictions"))).scalar() or 0
    if predictions > 0:
        logger.info("geo_intel.predictions already holds %d row(s) — nothing to do.", predictions)
        return False

    return True


async def main(grid_km: float, risk_threshold: int, if_needed: bool = False) -> int:
    try:
        async with async_session() as db:
            if if_needed and not await _should_run(db):
                return 0
            predictions = await geo_service.generate_hotspot_predictions(
                db,
                DEFAULT_BOUNDS,
                grid_km=grid_km,
                risk_threshold=risk_threshold,
            )
    finally:
        # Dispose inside this loop — the asyncpg pool is bound to it, and disposing
        # from a second asyncio.run() would touch an already-closed loop.
        await engine.dispose()

    if not predictions:
        # Not an error: the model ran and nothing in this viewport cleared the bar.
        logger.warning(
            "Model ran but no grid point scored >= %s, so no hotspots were stored. "
            "The map will show 0 zones. Lower --risk-threshold to widen the forecast.",
            risk_threshold,
        )
        return 0

    top = max(p["risk_score"] for p in predictions)
    logger.info(
        "Stored %d hotspot prediction(s) across the demo bounds (top risk score %s).",
        len(predictions),
        top,
    )
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grid-km", type=float, default=2.0, help="grid spacing in km (default: 2.0)")
    parser.add_argument(
        "--risk-threshold", type=int, default=50, help="only store points scoring at/above this (default: 50)"
    )
    parser.add_argument(
        "--if-needed",
        action="store_true",
        help="no-op unless incidents exist and predictions do not (used at container start)",
    )
    args = parser.parse_args()

    try:
        exit_code = asyncio.run(main(args.grid_km, args.risk_threshold, if_needed=args.if_needed))
    except Exception:
        # Fail loudly here rather than letting a missing model artifact or an
        # unreachable database surface later as a silently empty map.
        logger.exception("Failed to generate hotspot predictions")
        exit_code = 1

    sys.exit(exit_code)
