#!/bin/bash
set -e
make test
make sims
if python3 - <<'PY'
import os, sys, time, pathlib as p
key = os.getenv('FRED_API_KEY')
cache = p.Path('data/cache')
cache.mkdir(parents=True, exist_ok=True)
stamp = cache / 'fred_last_pull.stamp'
needs = not stamp.exists() or (time.time() - stamp.stat().st_mtime) > 7 * 86400
sys.exit(0 if (key and needs) else 1)
PY
then
PYTHONPATH=. python3 sims/make_macro_figs.py --start 1999-01-01 --end 2025-12-31 --output-dir figs --cache-dir data/cache
touch data/cache/fred_last_pull.stamp
fi
PYTHONPATH=. python3 sims/make_calibration_tables.py
make paper
python3 research/ci/robustness.py
