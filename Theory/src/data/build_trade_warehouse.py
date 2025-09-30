"""Builds a local trade data warehouse from BACI and CEPII gravity sources."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

RAW_BACI_DIR = Path("/Users/ian/trade_thesis_phd_final/pythonProject/data/raw/baci")
RAW_GRAVITY_DIR = Path("/Users/ian/trade_thesis_phd_final/pythonProject/data/raw/gravity")
DEFAULT_WAREHOUSE = Path("/Users/ian/trade_data_warehouse")


def _load_country_map() -> pd.Series:
    mapping = pd.read_csv(RAW_BACI_DIR / "country_codes_V202401b.csv")
    return mapping.set_index("country_code")["country_iso3"].astype(str)


def _iter_baci_files(years: Iterable[int] | None = None) -> Iterable[tuple[int, Path]]:
    files = sorted(RAW_BACI_DIR.glob("BACI_HS02_Y*_V202401b.csv"))
    for file in files:
        year = int(file.name.split("_Y")[1][:4])
        if years is None or year in years:
            yield year, file


def _aggregate_baci(years: Iterable[int] | None = None) -> pd.DataFrame:
    code_to_iso = _load_country_map()
    records = defaultdict(float)
    for year, path in _iter_baci_files(years):
        for chunk in pd.read_csv(
            path,
            usecols=["i", "j", "v"],
            chunksize=1_000_000,
            dtype={"i": np.int32, "j": np.int32, "v": np.float64},
        ):
            chunk["iso_o"] = chunk["i"].map(code_to_iso)
            chunk["iso_d"] = chunk["j"].map(code_to_iso)
            chunk = chunk.dropna(subset=["iso_o", "iso_d"])
            grouped = chunk.groupby(["iso_o", "iso_d"], as_index=False)["v"].sum()
            for row in grouped.itertuples(index=False):
                records[(year, row.iso_o, row.iso_d)] += float(row.v)
    if not records:
        return pd.DataFrame(columns=["year", "iso_o", "iso_d", "trade_value_usd_millions"])
    data = (
        pd.DataFrame(
            (
                {
                    "year": year,
                    "iso_o": iso_o,
                    "iso_d": iso_d,
                    "trade_value_usd_millions": value,
                }
                for (year, iso_o, iso_d), value in records.items()
            )
        )
        .sort_values(["year", "iso_o", "iso_d"])
        .reset_index(drop=True)
    )
    return data


def _export_baci(warehouse: Path, years: Iterable[int] | None = None) -> None:
    baci_dir = warehouse / "baci"
    baci_dir.mkdir(parents=True, exist_ok=True)
    totals = _aggregate_baci(years)
    if totals.empty:
        return
    totals.to_parquet(baci_dir / "baci_bilateral_totals.parquet", index=False)
    # Store metadata for provenance
    meta = pd.DataFrame(
        {
            "description": [
                "Trade values (USD millions) aggregated from BACI HS02 raw files",
                "Source files located under /Users/ian/trade_thesis_phd_final/pythonProject/data/raw/baci",
            ]
        }
    )
    meta.to_csv(baci_dir / "README.csv", index=False)

    # Optional: store product descriptions for mapping purposes
    products = pd.read_csv(RAW_BACI_DIR / "product_codes_HS02_V202401b.csv")
    products.to_parquet(baci_dir / "product_codes_hs02.parquet", index=False)

    countries = pd.read_csv(RAW_BACI_DIR / "country_codes_V202401b.csv")
    countries.to_parquet(baci_dir / "country_codes.parquet", index=False)


def _export_gravity(warehouse: Path) -> None:
    gravity_dir = warehouse / "gravity"
    gravity_dir.mkdir(parents=True, exist_ok=True)
    gravity = pd.read_csv(RAW_GRAVITY_DIR / "Gravity_V202211.csv")
    gravity.to_parquet(gravity_dir / "gravity_v202211.parquet", index=False)

    # Export supporting label tables for reference
    for label_file in RAW_GRAVITY_DIR.glob("Label_*.csv"):
        df = pd.read_csv(label_file)
        df.to_parquet(gravity_dir / f"{label_file.stem.lower()}.parquet", index=False)

    countries = pd.read_csv(RAW_GRAVITY_DIR / "Countries_V202211.csv")
    countries.to_parquet(gravity_dir / "gravity_countries.parquet", index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build local trade data warehouse.")
    parser.add_argument(
        "--warehouse",
        default=str(DEFAULT_WAREHOUSE),
        help="Directory where processed trade data will be stored.",
    )
    parser.add_argument(
        "--years",
        nargs="*",
        type=int,
        help="Optional list of years to process for BACI.",
    )
    args = parser.parse_args()

    warehouse = Path(args.warehouse).expanduser()
    warehouse.mkdir(parents=True, exist_ok=True)

    _export_baci(warehouse, args.years)
    _export_gravity(warehouse)


if __name__ == "__main__":
    main()
