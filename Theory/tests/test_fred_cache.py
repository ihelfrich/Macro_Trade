import sys

import pandas as pd

import sims.make_macro_figs as macro


def test_macro_cache_and_offline_flow(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    cache_dir = tmp_path / "data" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    out_dir = tmp_path / "out"

    def fake(series_id, start, end):
        dates = pd.date_range(start=start, end=end, freq="ME")
        values = pd.RangeIndex(len(dates)).astype(float)
        return pd.DataFrame({"date": dates, "value": values})

    monkeypatch.setattr(macro, "fred_series", fake)

    argv = [
        "make_macro_figs",
        "--start",
        "2020-01-01",
        "--end",
        "2020-03-31",
        "--output-dir",
        str(out_dir),
        "--cache-dir",
        str(cache_dir),
    ]
    monkeypatch.setattr(sys, "argv", argv)
    macro.main()

    for sid in macro.CORE_SERIES.values():
        assert (cache_dir / f"{sid}.csv").exists()

    def offline(*_, **__):  # pragma: no cover - offline branch
        raise RuntimeError("offline")

    monkeypatch.setattr(macro, "fred_series", offline)
    monkeypatch.setattr(sys, "argv", argv)
    macro.main()
