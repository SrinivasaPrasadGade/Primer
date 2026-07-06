"""
Generates spatiotemporal training data for the Hotspot Predictor (Random Forest).

The real inputs described in sumanth_windows_ml_infra.md 3.2.1 are:
  - NCRB "Crime in India" district-wise CSVs (Kaggle mirrors, manual download —
    ncrb.gov.in only publishes PDFs)
  - OSM ATM/bank density via osmnx (see fetch_geo_features.py)

Both require a manual step (a Kaggle account, or a live network call to the
Overpass API) that can't run unattended. Rather than block model development
on that, this script simulates a full crime history over a grid of cells
across the same 6 NCRB cybercrime hotspot cities used elsewhere in this repo
(ml/data_generation/generate_seed.py), with Poisson-distributed daily crime
counts driven by an urban-core gradient plus a heavy-tailed per-cell
"hotspot propensity" so a few cells are chronically hot, most aren't.

If real data has been dropped in, it's blended in automatically:
  - data/raw/geo_crime/*.csv         -> reweights per-city crime intensity
                                         (best-effort column sniffing; see
                                         data/raw/geo_crime/README.md)
  - ml/data_generation/cache/osm_geo_features.csv
                                      -> real bank_atm_density / population_density
                                         per grid cell (produced by fetch_geo_features.py)
Falls back to synthetic values wherever real data isn't present.

Features (per grid cell x day, matching sumanth_windows_ml_infra.md 4.4):
  latitude, longitude, crime_count_7d, crime_count_30d, population_density,
  bank_atm_density, day_of_week, month, avg_loss_amount_area
Label:
  is_hotspot — 1 if the cell's crime count over the NEXT 7 days is in the
  top quartile for its city (i.e. what a next-7-day hotspot predictor is
  trained to flag), 0 otherwise. Only trailing/current-day features are
  used as inputs, so the label never leaks into the feature window.

Run:
    cd ml/data_generation
    python generate_hotspot_data.py

Output: ml/hotspot-predictor/data/hotspot_training_data.csv
"""
import csv
import glob
import math
import os
from datetime import date, timedelta

import numpy as np

from geo_grid import CITIES, all_cells, city_center

random_seed = 42
np.random.seed(random_seed)

WARMUP_DAYS = 30    # trailing history needed before the first usable row
HISTORY_DAYS = 180  # usable rows emitted per cell
FORWARD_DAYS = 7     # days looked ahead to build the label
TOTAL_SIM_DAYS = WARMUP_DAYS + HISTORY_DAYS + FORWARD_DAYS
ANCHOR_START = date(2025, 1, 1)  # fixed anchor -> reproducible day_of_week/month

HOTSPOT_QUANTILE = 0.75  # top quartile of next-7-day crime counts -> hotspot

RAW_NCRB_GLOB = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "raw", "geo_crime", "*.csv"
)
OSM_CACHE_PATH = os.path.join(os.path.dirname(__file__), "cache", "osm_geo_features.csv")
OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "hotspot-predictor", "data", "hotspot_training_data.csv"
)


def load_ncrb_city_weights():
    """Best-effort blend of real NCRB district crime totals into city weights.

    Kaggle NCRB mirrors vary in column naming, so this sniffs for a
    state/city-like text column and a numeric crime-count-like column rather
    than assuming an exact schema. Silently falls back to the default
    CITIES weights if no matching file is found or it can't be parsed —
    the synthetic distribution already tracks real NCRB cybercrime hotspot
    shares (see generate_seed.py), so this is a refinement, not a requirement.
    """
    default_weights = {city: cfg["weight"] for city, cfg in CITIES.items()}
    files = glob.glob(RAW_NCRB_GLOB)
    if not files:
        return default_weights, False

    try:
        import pandas as pd

        totals = {city: 0.0 for city in CITIES}
        matched_any = False
        for path in files:
            df = pd.read_csv(path)
            text_cols = [c for c in df.columns if df[c].dtype == object]
            numeric_cols = [c for c in df.columns if np.issubdtype(df[c].dtype, np.number)]
            if not text_cols or not numeric_cols:
                continue
            count_col = max(numeric_cols, key=lambda c: df[c].sum())
            for city, cfg in CITIES.items():
                needle = city.lower()
                mask = df[text_cols].apply(
                    lambda col: col.astype(str).str.lower().str.contains(needle, na=False)
                ).any(axis=1)
                if mask.any():
                    totals[city] += float(df.loc[mask, count_col].sum())
                    matched_any = True

        if not matched_any or sum(totals.values()) == 0:
            return default_weights, False

        total = sum(totals.values())
        real_weights = {city: v / total for city, v in totals.items()}
        # Blend 70% real signal / 30% default prior so a thin/noisy CSV
        # can't wildly distort the distribution.
        blended = {
            city: 0.7 * real_weights[city] + 0.3 * default_weights[city] for city in CITIES
        }
        norm = sum(blended.values())
        return {city: w / norm for city, w in blended.items()}, True
    except Exception as exc:
        print(f"  (couldn't parse NCRB CSV, using default city weights: {exc})")
        return default_weights, False


def load_osm_cache():
    """Real per-cell ATM/bank + population density from fetch_geo_features.py, if present."""
    if not os.path.exists(OSM_CACHE_PATH):
        return {}
    import pandas as pd

    df = pd.read_csv(OSM_CACHE_PATH)
    return {
        (round(r.lat, 6), round(r.lon, 6)): (r.bank_atm_density, r.population_density)
        for r in df.itertuples()
    }


def build_cells(city_weights):
    """Precompute static per-cell attributes: position, urban factor, densities, lambda."""
    cells = []
    osm_overrides = load_osm_cache()

    for city, state, lat, lon in all_cells():
        cfg = CITIES[city]
        center_lat, center_lon = city_center(cfg)
        # Rough degrees->km conversion is fine at this scale; only used to
        # shape a smooth urban-core gradient, not for real geodesy.
        dist_km = math.hypot((lat - center_lat) * 111, (lon - center_lon) * 111 * 0.95)
        urban_factor = 1.0 + 3.0 * math.exp(-dist_km / 6.0)

        override = osm_overrides.get((lat, lon))
        if override:
            bank_atm_density, population_density = override
        else:
            population_density = float(
                np.clip(np.random.lognormal(math.log(3000 * urban_factor), 0.4), 500, 45000)
            )
            bank_atm_density = float(
                np.clip(np.random.lognormal(math.log(2.5 * urban_factor), 0.5), 0, 150)
            )

        hotspot_propensity = np.random.lognormal(0.0, 0.6)  # heavy tail: a few chronic hotspots
        base_daily_lambda = 0.06 * city_weights[city] * len(CITIES) * urban_factor * hotspot_propensity

        cells.append({
            "city": city,
            "state": state,
            "lat": lat,
            "lon": lon,
            "urban_factor": urban_factor,
            "population_density": round(population_density, 1),
            "bank_atm_density": round(bank_atm_density, 1),
            "daily_lambda": base_daily_lambda,
        })
    return cells


def simulate_cell_history(cell):
    """Poisson daily crime counts + lognormal per-incident loss, with a mild
    weekday seasonality (scam calls cluster on weekdays, per generate_seed.py's
    HOUR_WEIGHTS reasoning applied here at daily granularity)."""
    weekday_multiplier = np.array([1.1, 1.15, 1.15, 1.1, 1.05, 0.75, 0.7])  # Mon..Sun
    daily_counts = np.zeros(TOTAL_SIM_DAYS, dtype=np.int64)
    daily_loss = np.zeros(TOTAL_SIM_DAYS, dtype=np.float64)

    for t in range(TOTAL_SIM_DAYS):
        dow = (ANCHOR_START + timedelta(days=t)).weekday()
        lam = cell["daily_lambda"] * weekday_multiplier[dow]
        count = np.random.poisson(lam)
        daily_counts[t] = count
        if count > 0:
            # Higher-urban_factor cells skew toward smaller average losses per
            # incident (higher volume, lower-value UPI/QR fraud) vs. sparser
            # cells trending toward larger-ticket scams — keeps the feature
            # from perfectly correlating with density.
            mu = math.log(60000) - 0.15 * cell["urban_factor"]
            daily_loss[t] = np.sum(np.random.lognormal(mu, 0.8, size=count))

    return daily_counts, daily_loss


def rows_for_cell(cell):
    daily_counts, daily_loss = simulate_cell_history(cell)
    cum_count = np.concatenate(([0], np.cumsum(daily_counts)))
    cum_loss = np.concatenate(([0.0], np.cumsum(daily_loss)))

    city_avg_loss = float(daily_loss[daily_counts > 0].sum() / max(daily_counts.sum(), 1)) \
        if daily_counts.sum() > 0 else 15000.0

    rows = []
    for t in range(WARMUP_DAYS, WARMUP_DAYS + HISTORY_DAYS):
        count_7d = int(cum_count[t + 1] - cum_count[t - 6])
        count_30d = int(cum_count[t + 1] - cum_count[t - 29])
        loss_30d = float(cum_loss[t + 1] - cum_loss[t - 29])
        avg_loss = loss_30d / count_30d if count_30d > 0 else city_avg_loss
        count_next7 = int(cum_count[t + 8] - cum_count[t + 1])

        d = ANCHOR_START + timedelta(days=t)
        rows.append({
            "city": cell["city"],
            "state": cell["state"],
            "latitude": cell["lat"],
            "longitude": cell["lon"],
            "date": d.isoformat(),
            "day_of_week": d.weekday(),
            "month": d.month,
            "crime_count_7d": count_7d,
            "crime_count_30d": count_30d,
            "population_density": cell["population_density"],
            "bank_atm_density": cell["bank_atm_density"],
            "avg_loss_amount_area": round(avg_loss, 2),
            "_crime_count_next7": count_next7,  # consumed below, not a feature
        })
    return rows


def main():
    city_weights, used_real_ncrb = load_ncrb_city_weights()
    cells = build_cells(city_weights)

    rows = []
    for cell in cells:
        rows.extend(rows_for_cell(cell))

    # Per-city top-quartile threshold on next-7-day crime count -> hotspot label.
    by_city_next7 = {}
    for r in rows:
        by_city_next7.setdefault(r["city"], []).append(r["_crime_count_next7"])
    thresholds = {
        city: np.quantile(counts, HOTSPOT_QUANTILE) if max(counts) > 0 else 1
        for city, counts in by_city_next7.items()
    }

    for r in rows:
        r["is_hotspot"] = int(r["_crime_count_next7"] >= thresholds[r["city"]] and r["_crime_count_next7"] > 0)
        del r["_crime_count_next7"]

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fieldnames = [
        "city", "state", "latitude", "longitude", "date", "day_of_week", "month",
        "crime_count_7d", "crime_count_30d", "population_density", "bank_atm_density",
        "avg_loss_amount_area", "is_hotspot",
    ]
    with open(OUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    n_hotspot = sum(r["is_hotspot"] for r in rows)
    osm_used = os.path.exists(OSM_CACHE_PATH)
    print(
        f"Generated {len(rows)} rows across {len(cells)} grid cells / {len(CITIES)} cities "
        f"({n_hotspot} hotspot, {len(rows) - n_hotspot} non-hotspot) -> {OUT_PATH}"
    )
    print(f"  NCRB city weights: {'blended from data/raw/geo_crime/*.csv' if used_real_ncrb else 'synthetic default'}")
    print(f"  ATM/bank + population density: {'from OSM cache' if osm_used else 'synthetic default'}")
    if not osm_used:
        print("  -> run fetch_geo_features.py (needs internet + osmnx) for real OSM density, then re-run this script.")


if __name__ == "__main__":
    main()
