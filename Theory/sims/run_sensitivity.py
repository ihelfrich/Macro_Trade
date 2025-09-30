"""Sensitivity analysis for GE welfare results."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Iterable, List, Tuple

import matplotlib.pyplot as plt
import pandas as pd

from src.common.io import write_fig, write_table
from src.policy.simulate import ScenarioResult, run_policy_scenarios
from src.trade.calibration import CalibrationConfig, load_calibration


def _scale_network_elasticities(
    config: CalibrationConfig, factor: float
) -> CalibrationConfig:
    scaled = {k: v * factor for k, v in config.network_elasticities.items()}
    return CalibrationConfig(
        armington_theta=config.armington_theta.copy(),
        ces_sigma=config.ces_sigma.copy(),
        network_elasticities=scaled,
        groups=list(config.groups),
        metadata=dict(config.metadata),
        references=list(config.references),
    )


def _select_scenario(results: Iterable[ScenarioResult], name: str) -> ScenarioResult:
    for res in results:
        if res.name == name:
            return res
    return list(results)[-1]


def _summarise(label: str, scenario: ScenarioResult) -> dict:
    return {
        "Run": label,
        "Scenario": scenario.name,
        "FO_pct": scenario.fo_global * 100.0,
        "SO_pct": scenario.so_global * 100.0,
    }


def generate_sensitivity_outputs(
    output_dir: str | Path = ".",
    policy: str | Path = "sims/configs/policies/baseline.json",
    mrio_config: str | Path = "data/mrio_config.yaml",
    calibration_path: str | Path = "data/calibration.yaml",
    target_scenario: str = "Tariff Shock",
) -> pd.DataFrame:
    output_path = Path(output_dir)
    tables_dir = output_path / "tables"
    figs_dir = output_path / "figs"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figs_dir.mkdir(parents=True, exist_ok=True)
    base_calibration = load_calibration(calibration_path)

    runs: List[Tuple[str, CalibrationConfig, dict | None]] = [
        (
            "Elasticity -25%",
            _scale_network_elasticities(base_calibration, 0.75),
            None,
        ),
        ("Elasticity baseline", base_calibration, None),
        (
            "Elasticity +25%",
            _scale_network_elasticities(base_calibration, 1.25),
            None,
        ),
        ("Damping 0.20", base_calibration, {"damp": 0.20}),
        ("Damping 0.50", base_calibration, {"damp": 0.50}),
        ("Damping 0.80", base_calibration, {"damp": 0.80}),
    ]

    summaries = []
    for label, calibration, solver_kwargs in runs:
        results = run_policy_scenarios(
            policy_config_path=str(policy),
            mrio_config_path=str(mrio_config),
            output_dir=str(output_path),
            calibration=calibration,
            solver_kwargs=solver_kwargs,
            write_outputs=False,
        )
        scenario = _select_scenario(results, target_scenario)
        summaries.append(_summarise(label, scenario))

    df = pd.DataFrame(summaries)
    table_path = tables_dir / "world_welfare_sensitivity.tex"
    write_table(df[["Run", "FO_pct", "SO_pct"]].round(3), str(table_path))
    canonical_table = Path("tables") / "world_welfare_sensitivity.tex"
    canonical_table.parent.mkdir(parents=True, exist_ok=True)
    if table_path.resolve() != canonical_table.resolve():
        shutil.copy2(table_path, canonical_table)

    fig, ax = plt.subplots(figsize=(7, 4))
    x = range(len(df))
    width = 0.35
    ax.bar([i - width / 2 for i in x], df["FO_pct"], width=width, label="First order")
    ax.bar([i + width / 2 for i in x], df["SO_pct"], width=width, label="Second order")
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.set_xticks(list(x))
    ax.set_xticklabels(df["Run"], rotation=20, ha="right")
    ax.set_ylabel("Global welfare change (percent)")
    ax.set_title("Sensitivity of tariff counterfactual")
    ax.legend(frameon=False)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.4)
    fig.tight_layout()
    fig_path = figs_dir / "policy_sensitivity.png"
    write_fig(fig, str(fig_path))
    canonical_fig = Path("figs") / "policy_sensitivity.png"
    canonical_fig.parent.mkdir(parents=True, exist_ok=True)
    if fig_path.resolve() != canonical_fig.resolve():
        shutil.copy2(fig_path, canonical_fig)
    plt.close(fig)

    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Run welfare sensitivity analysis.")
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory where sensitivity outputs will be written.",
    )
    parser.add_argument(
        "--policy",
        default=None,
        help="Policy JSON file (preferred flag).",
    )
    parser.add_argument(
        "--policy-config",
        default=None,
        help="Alias for --policy (legacy flag).",
    )
    parser.add_argument(
        "--mrio-config",
        default="data/mrio_config.yaml",
        help="MRIO configuration YAML.",
    )
    parser.add_argument(
        "--calibration",
        default="data/calibration.yaml",
        help="Calibration YAML file.",
    )
    parser.add_argument(
        "--scenario",
        default="Tariff Shock",
        help="Policy scenario name to track.",
    )
    args = parser.parse_args()

    policy_path = (
        args.policy or args.policy_config or "sims/configs/policies/baseline.json"
    )

    generate_sensitivity_outputs(
        output_dir=args.output_dir,
        policy=policy_path,
        mrio_config=args.mrio_config,
        calibration_path=args.calibration,
        target_scenario=args.scenario,
    )


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
