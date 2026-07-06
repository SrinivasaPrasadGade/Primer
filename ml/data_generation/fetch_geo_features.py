"""
Fetches real geographic features (ATM/bank density, urban-activity density)
for the Hotspot Predictor grid via OpenStreetMap, using osmnx.

This is the "OSM / Census Data (The Features)" step from
sumanth_windows_ml_infra.md 3.2.1: rather than downloading all of India's
OSM extract, this queries the live Overpass API per grid cell (same cells
as ml/data_generation/geo_grid.py) so results merge back into
generate_hotspot_data.py by exact lat/lon.

Needs a live internet connection and osmnx installed (pip install -r
ml/requirements.txt). Overpass is rate-limited and occasionally times out,
so this writes results incrementally and skips cells already cached — safe
to re-run after an interruption.

True census population density isn't available via OSM; `population_density`
here is a proxy built from OSM POI density (amenities + shops per km^2,
rescaled) — a reasonable "population hub" signal, but not literal
people-per-km^2. Swap in real Census/WorldPop figures if that precision
matters later.

Run:
    cd ml/data_generation
    python fetch_geo_features.py

Output: ml/data_generation/cache/osm_geo_features.csv
Then re-run generate_hotspot_data.py to pick it up.
"""
import csv
import math
import os
import time

from geo_grid import GRID_STEP_DEG, all_cells

CACHE_PATH = os.path.join(os.path.dirname(__file__), "cache", "osm_geo_features.csv")
REQUEST_PAUSE_SEC = 1.0  # be polite to the shared Overpass API
POI_DENSITY_SCALE = 400  # calibrates the POI-density proxy into a population_density-like range

FIELDNAMES = ["city", "lat", "lon", "bank_atm_density", "population_density"]


def _features_from_bbox(ox, north, south, east, west, tags):
    """osmnx's bbox argument order/shape changed between 1.x and 2.x — support both."""
    try:
        return ox.features_from_bbox(north, south, east, west, tags=tags)
    except TypeError:
        return ox.features_from_bbox(bbox=(west, south, east, north), tags=tags)


def load_existing():
    if not os.path.exists(CACHE_PATH):
        return {}
    import pandas as pd

    df = pd.read_csv(CACHE_PATH)
    return {(round(r.lat, 6), round(r.lon, 6)): r._asdict() for r in df.itertuples(index=False)}


def fetch_cell(ox, lat, lon, step):
    half = step / 2
    north, south = lat + half, lat - half
    east, west = lon + half, lon - half
    area_km2 = (step * 111.0) * (step * 111.0 * math.cos(math.radians(lat)))

    try:
        bank_atm = _features_from_bbox(ox, north, south, east, west, {"amenity": ["atm", "bank"]})
        bank_atm_count = len(bank_atm)
    except Exception:
        bank_atm_count = 0

    try:
        poi = _features_from_bbox(ox, north, south, east, west, {"amenity": True, "shop": True})
        poi_count = len(poi)
    except Exception:
        poi_count = 0

    bank_atm_density = round(bank_atm_count / area_km2, 2)
    population_density = round((poi_count / area_km2) * POI_DENSITY_SCALE, 1)
    return bank_atm_density, population_density


def main():
    try:
        import osmnx as ox
    except ImportError:
        raise SystemExit(
            "osmnx is not installed. Run: pip install -r ../requirements.txt\n"
            "(osmnx pulls in geopandas/shapely; on Windows, installing via conda-forge "
            "is often smoother than pip if wheel builds fail.)"
        )

    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    cached = load_existing()
    cells = list(all_cells())
    print(f"{len(cells)} grid cells total, {len(cached)} already cached.")

    file_exists = os.path.exists(CACHE_PATH)
    with open(CACHE_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()

        fetched = 0
        for city, state, lat, lon in cells:
            key = (round(lat, 6), round(lon, 6))
            if key in cached:
                continue
            bank_atm_density, population_density = fetch_cell(ox, lat, lon, GRID_STEP_DEG)
            writer.writerow({
                "city": city, "lat": lat, "lon": lon,
                "bank_atm_density": bank_atm_density,
                "population_density": population_density,
            })
            f.flush()
            fetched += 1
            print(f"  [{fetched}] {city} ({lat}, {lon}) -> atm/bank density {bank_atm_density}, "
                  f"pop. proxy {population_density}")
            time.sleep(REQUEST_PAUSE_SEC)

    print(f"Done. Wrote/updated {CACHE_PATH}")


if __name__ == "__main__":
    main()
