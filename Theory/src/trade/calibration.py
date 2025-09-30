
"""Calibration scaffolding for multi-region GE applications."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Mapping

import yaml
import numpy as np
import pandas as pd


@dataclass
class StoneGearyGroup:
    """Container for Stone-Geary preference parameters."""

    name: str
    income: float
    alpha: np.ndarray
    gamma: np.ndarray


@dataclass
class CalibrationConfig:
    """Elasticity and preference parameters used in GE calibration."""

    armington_theta: Dict[str, float]
    ces_sigma: Dict[str, float]
    network_elasticities: Dict[str, float]
    groups: List[StoneGearyGroup] = field(default_factory=list)
    metadata: Mapping[str, str] = field(default_factory=dict)
    references: List[str] = field(default_factory=list)

    def theta_for(self, sector: str) -> float:
        return self.armington_theta.get(sector, self.armington_theta.get("default", 5.0))

    def sigma_for(self, sector: str) -> float:
        return self.ces_sigma.get(sector, self.ces_sigma.get("default", 1.0))

    def epsilon_for(self, sector: str) -> float:
        return self.network_elasticities.get(sector, self.network_elasticities.get("default", 1.0))


def load_calibration(path: str | Path = "data/calibration.yaml") -> CalibrationConfig:
    """Load calibration parameters from YAML, falling back to synthetic defaults."""

    cfg_path = Path(path)
    if not cfg_path.exists():
        return _synthetic_default()

    with cfg_path.open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}

    armington = _combine_default_and_overrides(raw.get("armington_theta", {}))
    sigma = _combine_default_and_overrides(raw.get("ces_sigma", {}))
    network = _combine_default_and_overrides(raw.get("network_elasticities", {}))

    groups: List[StoneGearyGroup] = []
    for name, payload in (raw.get("stone_geary_groups", {}) or {}).items():
        alpha = np.asarray(payload.get("alpha", []), dtype=float)
        gamma = np.asarray(payload.get("gamma", []), dtype=float)
        groups.append(
            StoneGearyGroup(
                name=name,
                income=float(payload.get("income", 100.0)),
                alpha=alpha,
                gamma=gamma,
            )
        )

    metadata = raw.get("metadata", {})
    references = list(raw.get("references", []))

    return CalibrationConfig(
        armington_theta=armington,
        ces_sigma=sigma,
        network_elasticities=network,
        groups=groups,
        metadata=metadata,
        references=references,
    )


def calibration_table(config: CalibrationConfig, sectors: Iterable[str]) -> pd.DataFrame:
    """Summarise sectoral elasticities for documentation tables."""

    records = []
    for sector in sectors:
        records.append(
            {
                "sector": sector,
                "theta_armington": config.theta_for(sector),
                "sigma_ces": config.sigma_for(sector),
                "epsilon_network": config.epsilon_for(sector),
            }
        )
    return pd.DataFrame.from_records(records)


def stone_geary_matrix(config: CalibrationConfig) -> pd.DataFrame:
    """Return Stone-Geary parameters by income group."""

    rows = []
    for group in config.groups:
        rows.append(
            {
                "group": group.name,
                "income": group.income,
                "alpha": group.alpha,
                "gamma": group.gamma,
            }
        )
    return pd.DataFrame(rows)


def _combine_default_and_overrides(block: Mapping[str, object]) -> Dict[str, float]:
    default = float(block.get("default", 1.0))
    overrides = {k: float(v) for k, v in (block.get("sector_overrides", {}) or {}).items()}
    overrides["default"] = default
    return overrides


def _synthetic_default() -> CalibrationConfig:
    armington = _combine_default_and_overrides(
        {"default": 5.0, "sector_overrides": {"sector_3": 4.5, "sector_7": 6.0}}
    )
    sigma = _combine_default_and_overrides({"default": 0.8})
    network = _combine_default_and_overrides({"default": 1.5})

    groups = [
        StoneGearyGroup(
            name="Baseline",
            income=100.0,
            alpha=np.full(10, 0.1),
            gamma=np.full(10, 1.0),
        )
    ]
    return CalibrationConfig(
        armington_theta=armington,
        ces_sigma=sigma,
        network_elasticities=network,
        groups=groups,
        metadata={"source": "synthetic"},
        references=[],
    )
