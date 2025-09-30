"""Engel curve estimation for Stone–Geary preferences."""

from __future__ import annotations

import re
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd


def natural_sort_labels(labels: Iterable[str]) -> List[str]:
    """Return labels sorted by their numeric suffix when present."""

    def _natural_key(label: str):
        parts = re.split(r"(\d+)", str(label))
        return [int(part) if part.isdigit() else part for part in parts if part]

    return sorted([str(label) for label in labels], key=_natural_key)


def estimate_sg_from_budgets(df: pd.DataFrame) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """Estimate Stone–Geary ``alpha`` and ``gamma`` by household group.

    The input ``df`` must contain columns ``group``, ``income``, ``good``,
    ``expenditure``, and optionally ``price``.  Within each ``group`` we
    estimate the linearised Engel curve ``exp = β₀ + β₁ y`` for every good,
    enforcing ``Σ β₁ = 1`` and solving the implied linear system for
    subsistence levels ``gamma``.

    Returns
    -------
    tuple(dict, dict)
        Dictionaries mapping group id → ``alpha`` and ``gamma`` arrays ordered
        by the alphabetical sort of good names.  We anchor the Stone–Geary
        subsistence bundle by assuming the lowest observed income in a group
        approximates the aggregate subsistence cost ``Σ p γ``.
    """

    required_cols = {"group", "income", "good", "expenditure"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Budget dataframe missing columns: {missing}")

    if "price" not in df.columns:
        df = df.assign(price=1.0)

    alpha_by_group: Dict[str, np.ndarray] = {}
    gamma_by_group: Dict[str, np.ndarray] = {}

    for group, gdf in df.groupby("group"):
        goods = natural_sort_labels(gdf["good"].unique())
        K = len(goods)

        beta0 = np.zeros(K)
        beta1 = np.zeros(K)
        prices = np.zeros(K)

        for idx, good in enumerate(goods):
            sub = gdf[gdf["good"] == good]
            income = sub["income"].to_numpy(dtype=float)
            exp = sub["expenditure"].to_numpy(dtype=float)
            price = sub["price"].iloc[0]
            prices[idx] = float(price)

            X = np.column_stack([np.ones_like(income), income])
            beta, *_ = np.linalg.lstsq(X, exp, rcond=None)
            beta0[idx], beta1[idx] = beta

        alpha = np.maximum(beta1, 0.0)
        alpha_sum = alpha.sum()
        if alpha_sum <= 0:
            alpha = np.full(K, 1.0 / K)
        else:
            alpha = alpha / alpha_sum

        # Anchor subsistence expenditure at the lowest observed income.
        G_hat = float(gdf["income"].min())
        gamma = (beta0 + alpha * G_hat) / prices
        gamma = np.maximum(gamma, 0.0)

        alpha_by_group[group] = alpha
        gamma_by_group[group] = gamma

    return alpha_by_group, gamma_by_group
