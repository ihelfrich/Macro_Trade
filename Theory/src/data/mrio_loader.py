"""MRIO loader that supports synthetic fixtures and on-disk datasets."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Tuple

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

MatrixTuple = Tuple[csr_matrix, np.ndarray, np.ndarray, Iterable[str], Iterable[str]]


def load_mrio(source: str = "SYNTH", year: int = 2018, path: str | Path = "data/") -> MatrixTuple:
    """Load an MRIO (multi-region input-output) dataset.

    Parameters
    ----------
    source : str, default ``"SYNTH"``
        Name of the dataset.  ``"SYNTH"`` builds a deterministic synthetic
        benchmark (3 regions × 10 sectors) used in CI.  Any other value
        attempts to read matrices from disk using the pattern
        ``{path}/{source.lower()}_{year}_*.{csv,feather,npz}``.
    year : int, default 2018
        Calendar year tag for real datasets.
    path : str or Path, default ``"data/"``
        Directory holding MRIO files.

    Returns
    -------
    tuple
        ``(A_csr, VA, Y, sectors, countries)`` where ``A_csr`` is a CSR
        matrix of intermediate coefficients, ``VA`` value added, ``Y``
        final demand, and ``sectors``/``countries`` are name lists.
    """

    path = Path(path)
    source_upper = source.upper()
    if source_upper == "SYNTH":
        return _synthetic_mrio()
    if source_upper == "OECD_SML":
        return _load_oecd_sml(path, year)

    base = f"{source.lower()}_{year}"
    A_path = _find_file(path, base + "_A")
    VA_path = _find_file(path, base + "_VA")
    Y_path = _find_file(path, base + "_Y")

    if not (A_path and VA_path and Y_path):
        # Fall back to synthetic if any component missing
        return _synthetic_mrio()

    A = _load_matrix(A_path)
    VA = _load_vector(VA_path)
    Y = _load_vector(Y_path)

    K = A.shape[0]
    if A.shape[1] != K:
        raise ValueError("MRIO technology matrix must be square.")
    if VA.shape[0] != K or Y.shape[0] != K:
        raise ValueError("Value-added and final demand must align with A.")

    sectors_path = _find_file(path, base + "_sectors")
    countries_path = _find_file(path, base + "_countries")

    regions, sectors_count = _default_dimensions(K)
    sectors = (
        _load_labels(sectors_path, expected=sectors_count)
        if sectors_path
        else [f"sector_{i+1}" for i in range(sectors_count)]
    )
    countries = (
        _load_labels(countries_path, expected=regions)
        if countries_path
        else [f"country_{i+1}" for i in range(regions)]
    )

    return csr_matrix(A), VA, Y, sectors, countries


# ---------------------------------------------------------------------------
# Synthetic fixture
# ---------------------------------------------------------------------------


def _synthetic_mrio() -> MatrixTuple:
    n_regions = 3
    n_sectors = 10
    K = n_regions * n_sectors

    data = np.zeros((K, K), dtype=float)
    for col in range(K):
        region_c, sector_c = divmod(col, n_sectors)
        column = np.empty(K, dtype=float)
        for row in range(K):
            region_r, sector_r = divmod(row, n_sectors)
            weight = 0.006  # baseline spillover
            if region_r == region_c:
                weight += 0.010
            if sector_r == sector_c:
                weight += 0.012
            if row == col:
                weight += 0.045
            if abs(region_r - region_c) == 1:
                weight += 0.004
            column[row] = weight
        column_sum = column.sum()
        data[:, col] = 0.62 * column / column_sum  # keep spectral radius < 1

    A_csr = csr_matrix(data)

    # Value added/non-tradable components. Scale so GDP ≈ 1e5.
    sectors = [f"sector_{i+1}" for i in range(n_sectors)]
    countries = [f"country_{i+1}" for i in range(n_regions)]

    base_va = np.linspace(80.0, 140.0, n_sectors)
    VA = np.tile(base_va, n_regions) * (1.0 + 0.05 * np.repeat(np.arange(n_regions), n_sectors))
    Y = 0.4 * VA

    return A_csr, VA.astype(float), Y.astype(float), sectors, countries


# ---------------------------------------------------------------------------
# OECD SML processing
# ---------------------------------------------------------------------------


def _load_oecd_sml(path: Path, year: int) -> MatrixTuple:
    csv_path = path / f"{year}_SML.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"OECD SML CSV not found: {csv_path}")

    cache_dir = path / "processed"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"oecd_sml_{year}.npz"

    if cache_path.exists() and cache_path.stat().st_mtime >= csv_path.stat().st_mtime:
        data = np.load(cache_path, allow_pickle=True)
        A_csr = csr_matrix((data["data"], data["indices"], data["indptr"]), shape=tuple(data["shape"]))
        VA = data["VA"].astype(float)
        Y = data["Y"].astype(float)
        sectors = data["sectors"].tolist()
        countries = data["countries"].tolist()
        return A_csr, VA, Y, sectors, countries

    A_csr, VA, Y, sectors, countries = _process_oecd_sml(csv_path)
    np.savez(
        cache_path,
        data=A_csr.data,
        indices=A_csr.indices,
        indptr=A_csr.indptr,
        shape=A_csr.shape,
        VA=VA,
        Y=Y,
        sectors=np.array(sectors, dtype="U"),
        countries=np.array(countries, dtype="U"),
    )
    return A_csr, VA, Y, sectors, countries


def _process_oecd_sml(csv_path: Path) -> MatrixTuple:
    df = pd.read_csv(csv_path)
    if "V1" not in df.columns:
        raise ValueError("Expected column 'V1' with row identifiers in OECD SML file.")

    df = df.fillna(0.0)
    df = df.set_index("V1")

    industry_labels = [label for label in df.index if label not in {"VA", "OUT"} and label in df.columns]
    if not industry_labels:
        raise ValueError("Failed to locate industry rows/columns in OECD SML file.")

    first_country = industry_labels[0].split("_", 1)[0]
    sectors = [label.split("_", 1)[1] for label in industry_labels if label.startswith(first_country + "_")]
    countries = []
    for label in industry_labels:
        country = label.split("_", 1)[0]
        if country not in countries:
            countries.append(country)

    expected_labels = [f"{country}_{sector}" for country in countries for sector in sectors]
    missing = [label for label in expected_labels if label not in industry_labels]
    if missing:
        raise ValueError(f"OECD SML data missing industry entries: {missing[:5]} ...")

    industry_block = df.loc[expected_labels, expected_labels].astype(float)
    Z = industry_block.to_numpy(dtype=float)

    final_demand_cols = [col for col in df.columns if col not in expected_labels and col != "OUT"]
    final_demand = df.loc[expected_labels, final_demand_cols].astype(float).sum(axis=1).to_numpy(dtype=float)

    outputs = df.loc["OUT", expected_labels].to_numpy(dtype=float)
    value_added = df.loc["VA", expected_labels].to_numpy(dtype=float)

    A = np.zeros_like(Z)
    nonzero = outputs > 0
    A[:, nonzero] = Z[:, nonzero] / outputs[nonzero]

    A_csr = csr_matrix(A)
    return A_csr, value_added, final_demand, sectors, countries


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------


def _find_file(path: Path, stem: str) -> Path | None:
    for ext in (".npz", ".npy", ".csv", ".feather", ".parquet"):
        candidate = path / f"{stem}{ext}"
        if candidate.exists():
            return candidate
    return None


def _load_matrix(path: Path) -> np.ndarray:
    if path.suffix == ".npz":
        loaded = np.load(path)
        if isinstance(loaded, np.lib.npyio.NpzFile):
            if "arr_0" not in loaded:
                raise ValueError(f"NPZ file {path} missing 'arr_0'.")
            return np.asarray(loaded["arr_0"], dtype=float)
        return np.asarray(loaded, dtype=float)
    if path.suffix == ".npy":
        return np.load(path)
    if path.suffix in (".csv", ".txt"):
        return pd.read_csv(path, header=None).to_numpy(dtype=float)
    if path.suffix in (".feather", ".parquet"):
        df = pd.read_feather(path) if path.suffix == ".feather" else pd.read_parquet(path)
        return df.to_numpy(dtype=float)
    raise ValueError(f"Unsupported matrix format for {path}.")


def _load_vector(path: Path) -> np.ndarray:
    if path.suffix == ".npz":
        loaded = np.load(path)
        if isinstance(loaded, np.lib.npyio.NpzFile):
            if "arr_0" not in loaded:
                raise ValueError(f"NPZ file {path} missing 'arr_0'.")
            data = loaded["arr_0"]
        else:
            data = loaded
        return np.asarray(data, dtype=float).reshape(-1)
    if path.suffix == ".npy":
        return np.load(path).reshape(-1)
    if path.suffix in (".csv", ".txt"):
        return pd.read_csv(path, header=None).iloc[:, 0].to_numpy(dtype=float)
    if path.suffix in (".feather", ".parquet"):
        df = pd.read_feather(path) if path.suffix == ".feather" else pd.read_parquet(path)
        if df.shape[1] != 1:
            raise ValueError(f"Vector file {path} must have a single column.")
        return df.iloc[:, 0].to_numpy(dtype=float)
    raise ValueError(f"Unsupported vector format for {path}.")


def _load_labels(path: Path, expected: int) -> list[str]:
    if path.suffix in (".csv", ".txt"):
        labels = pd.read_csv(path, header=None).iloc[:, 0].astype(str).tolist()
    elif path.suffix in (".feather", ".parquet"):
        df = pd.read_feather(path) if path.suffix == ".feather" else pd.read_parquet(path)
        if df.shape[1] != 1:
            raise ValueError(f"Label file {path} must have exactly one column.")
        labels = df.iloc[:, 0].astype(str).tolist()
    else:
        raise ValueError(f"Unsupported label format for {path}.")

    if len(labels) != expected:
        raise ValueError(f"Expected {expected} labels in {path}, found {len(labels)}.")
    return labels


def _default_dimensions(K: int) -> tuple[int, int]:
    if K == 0:
        return 0, 0
    if K % 10 == 0:
        sectors = 10
    elif K % 8 == 0:
        sectors = 8
    else:
        sectors = max(1, int(round(np.sqrt(K))))
        while K % sectors != 0 and sectors > 1:
            sectors -= 1
    regions = max(1, K // sectors)
    return regions, sectors
