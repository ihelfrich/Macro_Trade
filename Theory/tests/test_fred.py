import pandas as pd
import pytest

from src.data.fred import fred_series
import sims.make_macro_figs as macro


def test_fred_series_requires_key(monkeypatch):
    monkeypatch.delenv("FRED_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        fred_series("CPIAUCSL", "2020-01-01", "2020-12-31")


def test_synthetic_series_generation():
    df = macro._synthetic_series("2020-01-01", "2020-12-31")
    assert not df.empty
    assert isinstance(df.iloc[0]["date"], pd.Timestamp)


def test_cached_series_used_when_fred_unavailable(tmp_path, monkeypatch):
    cache_file = tmp_path / "CPIAUCSL.csv"
    synthetic = macro._synthetic_series("2020-01-01", "2020-12-31")
    synthetic.to_csv(cache_file, index=False)

    def _raise(*args, **kwargs):  # pragma: no cover - injected behaviour
        raise RuntimeError("FRED unavailable")

    monkeypatch.setattr(macro, "fred_series", _raise)

    df = macro._load_series("CPIAUCSL", "2020-01-01", "2020-12-31", tmp_path)
    assert not df.empty
    assert cache_file.exists()
