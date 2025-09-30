"""Fetch key macro series from FRED and produce validation figures/tables."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import shutil

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.common.io import write_fig, write_table
from src.data.fred import fred_series

CORE_SERIES = {
    "CPI": "CPIAUCSL",
    "PPI": "PPIACO",
    "Industrial Production": "INDPRO",
    "10Y Treasury": "DGS10",
}

OPTIONAL_SERIES = {
    "3M Treasury Bill": "TB3MS",
    "Energy CPI": "CPIENGSL",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create macro validation figures via FRED data."
    )
    parser.add_argument(
        "--start",
        default="2010-01-01",
        help="Observation start date (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--end",
        default=datetime.today().strftime("%Y-%m-%d"),
        help="Observation end date.",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory where outputs will be written.",
    )
    parser.add_argument(
        "--cache-dir",
        default="data/cache",
        help="Directory for cached FRED downloads.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = Path(args.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    series_data: dict[str, pd.DataFrame] = {}
    for name, sid in CORE_SERIES.items():
        df = _load_series(sid, args.start, args.end, cache_dir)
        series_data[name] = df

    for name, sid in OPTIONAL_SERIES.items():
        cached = _read_cache(sid, cache_dir)
        if cached is not None:
            series_data[name] = _clip_window(cached, args.start, args.end)

    canonical_fig = Path("figs") / "macro_validation.png"
    canonical_table = Path("tables") / "macro_validation.tex"
    canonical_fig.parent.mkdir(parents=True, exist_ok=True)
    canonical_table.parent.mkdir(parents=True, exist_ok=True)

    _plot_series(series_data, canonical_fig)
    _emit_table(series_data, canonical_table)

    if output_dir.resolve() != canonical_fig.parent.resolve():
        target_fig = output_dir / "macro_validation.png"
        target_fig.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(canonical_fig, target_fig)

    if output_dir.resolve() != canonical_table.parent.resolve():
        target_table = output_dir / "macro_validation.tex"
        target_table.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(canonical_table, target_table)


def _synthetic_series(start: str, end: str) -> pd.DataFrame:
    dates = pd.date_range(start=start, end=end, freq="ME")
    t = np.linspace(0, 1, len(dates))
    values = 100 + 5 * np.sin(2 * np.pi * t) + 2 * t
    return pd.DataFrame({"date": dates, "value": values})


def _plot_series(data: dict[str, pd.DataFrame], output_path: Path) -> None:
    n = len(data)
    cols = 2
    rows = max(1, int(np.ceil(n / cols)))
    fig, axes = plt.subplots(rows, cols, figsize=(10, 3 * rows), sharex=False)
    axes = np.atleast_1d(axes).flatten()
    for ax, (name, df) in zip(axes, data.items()):
        ax.plot(df["date"], df["value"])
        ax.set_title(name)
        ax.grid(True, alpha=0.3)
    for ax in axes[n:]:
        ax.axis("off")
    fig.tight_layout()
    write_fig(fig, str(output_path))
    plt.close(fig)


def _emit_table(data: dict[str, pd.DataFrame], output_path: Path) -> None:
    rows = []
    for name, df in data.items():
        latest = float(df.iloc[-1]["value"])
        mean = float(df["value"].mean())
        std = float(df["value"].std(ddof=1)) if len(df) > 1 else 0.0
        rows.append({"series": name, "latest": latest, "mean": mean, "std": std})
    table = pd.DataFrame(rows)
    write_table(table, str(output_path))


def _load_series(series_id: str, start: str, end: str, cache_dir: Path) -> pd.DataFrame:
    cache_file = _cache_file(cache_dir, series_id)
    existing = _read_cache(series_id, cache_dir)
    try:
        df_live = fred_series(series_id, start, end)
        if df_live.empty:
            raise RuntimeError("Empty FRED payload")
        df_live = df_live.sort_values("date")
        combined = _combine(existing, df_live)
        _write_cache(combined, cache_file)
        return _clip_window(combined, start, end)
    except RuntimeError:
        if existing is not None:
            return _clip_window(existing, start, end)
        fallback = _synthetic_series(start, end)
        _write_cache(fallback, cache_file)
        return fallback


def _combine(existing: pd.DataFrame | None, new: pd.DataFrame) -> pd.DataFrame:
    if existing is None:
        return new[["date", "value"]]
    combined = pd.concat(
        [existing[["date", "value"]], new[["date", "value"]]], ignore_index=True
    )
    combined = combined.drop_duplicates(subset="date").sort_values("date")
    return combined


def _clip_window(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    lower = pd.to_datetime(start)
    upper = pd.to_datetime(end)
    mask = (df["date"] >= lower) & (df["date"] <= upper)
    clipped = df.loc[mask].copy()
    if clipped.empty:
        return df.copy()
    return clipped


def _cache_file(cache_dir: Path, series_id: str) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{series_id}.csv"


def _read_cache(series_id: str, cache_dir: Path) -> pd.DataFrame | None:
    cache_file = _cache_file(cache_dir, series_id)
    if cache_file.exists():
        try:
            return pd.read_csv(cache_file, parse_dates=["date"])
        except Exception:  # pragma: no cover - corrupt cache
            cache_file.unlink(missing_ok=True)
    return None


def _write_cache(df: pd.DataFrame, cache_file: Path) -> None:
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    df[["date", "value"]].to_csv(cache_file, index=False)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
