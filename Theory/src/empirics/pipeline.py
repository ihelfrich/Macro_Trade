
"""Synthetic data generators for empirics scaffolding."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd


@dataclass
class StaggeredConfig:
    units: int = 60
    periods: int = 16
    early_adopt: int = 6
    late_adopt: int = 10
    effect: float = 1.0
    seed: int = 0


def synthetic_staggered_panel(cfg: StaggeredConfig | None = None) -> pd.DataFrame:
    """Generate a Sun--Abraham style panel with clean pre-trends."""

    cfg = cfg or StaggeredConfig()
    rng = np.random.default_rng(cfg.seed)
    units = np.arange(cfg.units)
    periods = np.arange(cfg.periods)

    adoption = np.full(cfg.units, np.inf)
    half = cfg.units // 2
    adoption[: half] = cfg.early_adopt
    adoption[half : half + cfg.units // 3] = cfg.late_adopt

    rows = []
    for i in units:
        base = rng.normal(0.0, 0.5, size=cfg.periods)
        for t, base_shock in zip(periods, base):
            treated = float(t >= adoption[i]) if np.isfinite(adoption[i]) else 0.0
            outcome = 0.2 * i / cfg.units + 0.1 * t + base_shock
            if treated:
                outcome += cfg.effect
            rows.append(
                {
                    'i': int(i),
                    't': int(t),
                    'D': treated,
                    'y': float(outcome),
                    'adoption': adoption[i],
                }
            )
    return pd.DataFrame(rows)


def synthetic_iv_dataset(n: int = 400, strength: float = 0.6, seed: int = 1) -> Dict[str, np.ndarray]:
    """Return arrays for IV diagnostics with adjustable instrument strength."""    
    rng = np.random.default_rng(seed)
    z1 = rng.normal(size=n)
    z2 = rng.normal(size=n)
    cluster = np.floor(np.linspace(0, max(1, n // 20) - 1, n)).astype(int)
    u = rng.normal(scale=0.5, size=n)
    x = strength * z1 + strength * 0.5 * z2 + u
    eps = rng.normal(scale=0.5, size=n)
    y = 2.0 * x + 0.3 * u + eps
    Z = np.column_stack([z1, z2])
    return {'y': y, 'x': x, 'Z': Z, 'cluster': cluster}


def synthetic_budget_data(groups: Iterable[str] = ('Low', 'Middle', 'High'), sectors: int = 10, seed: int = 2) -> pd.DataFrame:
    """Create a Stone-Geary compatible expenditure dataset."""

    rng = np.random.default_rng(seed)
    rows = []
    base_prices = np.linspace(0.8, 1.5, sectors)
    for g_idx, group in enumerate(groups):
        income = 60 + 60 * g_idx
        alpha = rng.dirichlet(np.ones(sectors))
        gamma = np.linspace(0.5, 1.5, sectors) * (0.8 + 0.1 * g_idx)
        for h in range(80):
            income_draw = income + rng.normal(scale=5.0)
            for s in range(sectors):
                price = base_prices[s]
                expend = price * (gamma[s] + alpha[s] * max(income_draw - price * gamma.sum(), 0.0) / price)
                rows.append(
                    {
                        'group': group,
                        'household': f'{group}_{h}',
                        'good': f'sector_{s+1}',
                        'income': income_draw,
                        'price': price,
                        'expenditure': expend,
                    }
                )
    return pd.DataFrame(rows)
