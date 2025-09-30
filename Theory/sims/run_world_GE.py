"""CLI entry point for the global GE policy counterfactual pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.policy.simulate import run_policy_scenarios


def main():
    parser = argparse.ArgumentParser(description="Run global GE policy simulations.")
    parser.add_argument(
        "--config",
        default=str(Path('sims') / 'configs' / 'policies' / 'baseline.json'),
        help="Path to the policy scenario JSON configuration.",
    )
    parser.add_argument(
        "--mrio-config",
        default=str(Path('data') / 'mrio_config.yaml'),
        help="Path to MRIO configuration YAML file.",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory where tables/ and figs/ outputs will be written.",
    )
    parser.add_argument(
        "--calibration",
        default=str(Path('data') / 'calibration.yaml'),
        help="Path to calibration YAML (elasticities, Stone-Geary groups).",
    )
    args = parser.parse_args()

    run_policy_scenarios(
        policy_config_path=args.config,
        mrio_config_path=args.mrio_config,
        output_dir=args.output_dir,
        calibration_path=args.calibration,
    )


if __name__ == "__main__":
    main()
