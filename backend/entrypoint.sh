#!/bin/sh
set -e

alembic upgrade head

# Populate geo_intel.predictions when the database has incidents but no forecast.
# Nothing else writes that table, so without this the Geo Intel map reports
# 0 predicted hotspots until someone runs the generator by hand.
#
# --if-needed makes this a no-op on an unseeded database: 01_seed.sql is loaded
# manually AFTER the migrations (see sumanth_windows_ml_infra.md §3.2.2), so on a
# first boot there is nothing to forecast from and the next start picks it up
# instead. Failures are logged, never fatal — a missing model artifact should
# degrade the map, not stop the API serving every other module.
python -m scripts.bootstrap_predictions --if-needed \
    || echo "WARNING: hotspot bootstrap failed; Geo Intel will show 0 zones until it is run manually."

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
