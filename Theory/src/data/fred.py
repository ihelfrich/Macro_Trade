"""Thin wrapper around the FRED API with basic rate-limit handling."""

from __future__ import annotations

import json
import os
import time
from datetime import datetime
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd

_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


def fred_series(series_id: str, start: str, end: Optional[str] = None) -> pd.DataFrame:
    """Fetch a FRED time series between ``start`` and ``end`` (ISO dates)."""

    api_key = os.getenv('FRED_API_KEY')
    if not api_key:
        raise RuntimeError("FRED_API_KEY not set in environment")

    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start,
    }
    if end:
        params['observation_end'] = end

    query = f"{_BASE_URL}?{urlencode(params)}"

    backoff = 1.0
    for attempt in range(3):
        try:
            with urlopen(query, timeout=10) as resp:  # nosec - trusted domain
                payload = json.loads(resp.read().decode('utf-8'))
            break
        except HTTPError as exc:
            if exc.code == 429 and attempt < 2:
                time.sleep(backoff)
                backoff *= 2
                continue
            raise RuntimeError(f"FRED request failed ({exc.code})") from exc
        except URLError as exc:  # pragma: no cover - transient network failure
            if attempt < 2:
                time.sleep(backoff)
                backoff *= 2
                continue
            raise RuntimeError("FRED request failed") from exc
    else:  # pragma: no cover - loop exhausted
        raise RuntimeError("Unable to retrieve data from FRED")

    observations = payload.get('observations', [])
    if not observations:
        return pd.DataFrame(columns=['date', 'value'])

    dates = []
    values = []
    for obs in observations:
        dates.append(datetime.strptime(obs['date'], '%Y-%m-%d'))
        val = obs.get('value', '.')
        try:
            values.append(float(val))
        except ValueError:
            values.append(float('nan'))

    return pd.DataFrame({'date': pd.to_datetime(dates), 'value': values})
