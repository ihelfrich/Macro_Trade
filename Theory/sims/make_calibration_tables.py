"""Generate calibration summary tables for the GE model."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from src.common.io import write_table
from src.data.mrio_loader import load_mrio
from src.trade.calibration import (
    load_calibration,
    calibration_table,
    stone_geary_matrix,
)


def format_vector(values: np.ndarray, max_items: int = 6) -> str:
    arr = np.asarray(values, dtype=float)
    if arr.size <= max_items:
        body = ", ".join(f"{v:.2f}" for v in arr)
    else:
        head = ", ".join(f"{v:.2f}" for v in arr[: max_items - 1])
        body = f"{head}, …, {arr[-1]:.2f}"
    return f"[{body}]"


def generate_calibration_tables(
    calibration_path: str,
    mrio_config: str,
    output_dir: str,
) -> None:
    calibration = load_calibration(calibration_path)
    mrio_cfg = _load_yaml(mrio_config)
    A_csr, VA, Y, sectors, countries = load_mrio(**mrio_cfg.get("mrio", {}))

    calib_df = calibration_table(calibration, sectors).round(3)
    calib_df['sector'] = calib_df['sector'].str.replace('_', ' ', regex=False)
    calib_df = calib_df.rename(
        columns={
            'sector': 'Sector',
            'theta_armington': 'Armington theta',
            'sigma_ces': 'CES sigma',
            'epsilon_network': 'Network epsilon',
        }
    )
    write_table(calib_df, str(Path(output_dir) / "tables" / "calibration_params.tex"))

    sg_df = stone_geary_matrix(calibration)
    if sg_df.empty:
        sg_df = _synthetic_summary(countries, sectors)
    else:
        sg_df = sg_df.copy()
        sg_df["alpha"] = sg_df["alpha"].apply(format_vector)
        sg_df["gamma"] = sg_df["gamma"].apply(format_vector)
    write_table(sg_df, str(Path(output_dir) / "tables" / "stone_geary_groups.tex"))


def _synthetic_summary(countries: Iterable[str], sectors: Iterable[str]) -> pd.DataFrame:
    size = len(countries) * len(sectors)
    alpha = np.full(size, 1.0 / size)
    gamma = np.full(size, 0.2)
    return pd.DataFrame(
        {
            "group": ["Baseline"],
            "income": [100.0],
            "alpha": [format_vector(alpha)],
            "gamma": [format_vector(gamma)],
        }
    )


def _load_yaml(path: str) -> dict:
    import yaml

    with Path(path).open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate calibration tables")
    parser.add_argument(
        "--calibration",
        default="data/calibration.yaml",
        help="Calibration YAML file",
    )
    parser.add_argument(
        "--mrio-config",
        default="data/mrio_config.yaml",
        help="MRIO configuration YAML",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory where tables/ will be written",
    )
    args = parser.parse_args()

    generate_calibration_tables(args.calibration, args.mrio_config, args.output_dir)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
