"""
Shared spatial grid for the Hotspot Predictor pipeline.

generate_hotspot_data.py (synthetic crime history) and fetch_geo_features.py
(real OSM ATM/bank density) must produce cells at identical lat/lon
centroids so the two sources can be merged by exact coordinate match.

City bounding boxes and weights match ml/data_generation/generate_seed.py's
CITIES table (extended with Chennai/Pune per the NCRB 2024 cybercrime
hotspot spread documented in sumanth_windows_ml_infra.md section 3.2.1).
"""

CITIES = {
    "Mumbai":    {"lat": (18.90, 19.28), "lon": (72.77, 72.98), "state": "Maharashtra", "weight": 0.25},
    "Delhi":     {"lat": (28.50, 28.78), "lon": (76.95, 77.35), "state": "Delhi",       "weight": 0.22},
    "Bangalore": {"lat": (12.85, 13.10), "lon": (77.50, 77.70), "state": "Karnataka",   "weight": 0.18},
    "Hyderabad": {"lat": (17.30, 17.50), "lon": (78.35, 78.55), "state": "Telangana",   "weight": 0.15},
    "Chennai":   {"lat": (12.95, 13.15), "lon": (80.15, 80.30), "state": "Tamil Nadu",  "weight": 0.10},
    "Pune":      {"lat": (18.45, 18.60), "lon": (73.80, 73.95), "state": "Maharashtra", "weight": 0.10},
}

GRID_STEP_DEG = 0.05  # ~5km cells at these latitudes


def city_center(cfg):
    lat_min, lat_max = cfg["lat"]
    lon_min, lon_max = cfg["lon"]
    return (lat_min + lat_max) / 2, (lon_min + lon_max) / 2


def city_grid_cells(cfg, step=GRID_STEP_DEG):
    """Yield (lat, lon) centroids covering a city's bounding box."""
    lat_min, lat_max = cfg["lat"]
    lon_min, lon_max = cfg["lon"]
    lat = lat_min + step / 2
    while lat < lat_max:
        lon = lon_min + step / 2
        while lon < lon_max:
            yield round(lat, 6), round(lon, 6)
            lon += step
        lat += step


def all_cells(step=GRID_STEP_DEG):
    """Yield (city, state, lat, lon) for every grid cell across all cities."""
    for city, cfg in CITIES.items():
        for lat, lon in city_grid_cells(cfg, step):
            yield city, cfg["state"], lat, lon
