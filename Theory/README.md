# Fragmented Globalization Toolkit

This repository contains the code that accompanies *Fragmented Globalization: Theory, Measurement, and Policy*. It couples a globally convergent general-equilibrium core with sparse multi-region input–output infrastructure, Stone–Geary distributional analytics, granular exposure diagnostics, modern econometric utilities, and an automated policy-counterfactual laboratory.

## What lives where

- `src/trade/` – GE solvers (`solve_ge`), Domar weights, Baqaee–Farhi welfare corrections, and Stone–Geary equivalent variation.
- `src/common/` – sparse Leontief solves and I/O helpers.
- `src/data/` – MRIO loader plus `fred_series` for macro validation.
- `src/empirics/` – Sun–Abraham event studies, clustered IV diagnostics, granular concentration utilities.
- `src/policy/` – high-level simulator that turns policy JSONs into tables and figures.
- `sims/` – reproducible scripts: `run_world_GE.py` for policy experiments, `make_empirics.py` for Sun–Abraham and IV diagnostics, `run_sensitivity.py` for GE sensitivity sweeps, `make_distributional.py` for Stone–Geary estimation, and `make_macro_figs.py` for FRED comparisons.
- `sims/configs/policies/` – example scenario definitions (baseline + illustrative shocks).
- `data/mrio_config.yaml` – MRIO source declaration (defaults to the synthetic benchmark used in CI).
- `paper/` – Econometrica-style manuscript that ingests the generated tables and figures.

## Getting started

Create an environment with the dependencies listed in `CONDA_ENV.yml` or `requirements.txt`. The CI suite assumes Python 3.12.

## Reproducing the full stack

```bash
bash ci/run_all.sh
```

That script executes

1. unit tests (`make test`),
2. the simulation suite in `sims/` (tri-node, IO amplification, granular exposure, Stone–Geary dispersion, empirics, and GE sensitivities),
3. calibration-summary tables via `sims/make_calibration_tables.py`,
4. a full LaTeX build of the paper,
5. and a light robustness placeholder in `research/ci/`.

All tables land in `tables/` as LaTeX files and all figures live in `figs/`.

### Policy counterfactuals

Edit or extend `sims/configs/policies/*.json` to describe tariffs, sanctions, reroute multipliers, CBAM adjustments, or FX pass-through. Then run

```bash
python sims/run_world_GE.py --config sims/configs/policies/baseline.json \
                             --mrio-config data/mrio_config.yaml \
                             --output-dir .
```

The script emits `tables/world_welfare.tex`, `tables/distributional_incidence.tex`, `figs/policy_scenarios.png`, and `figs/map_global_welfare.png`.

### Empirical outputs

To regenerate the Sun–Abraham event-study tables and clustered IV diagnostics (with synthetic fallbacks pending real data) run

```bash
python sims/make_empirics.py --output-dir .
```

This writes `tables/es_main.tex`, `tables/es_pretrend.tex`, `tables/iv_main.tex`, and the associated figures `figs/event_study.png` and `figs/iv_diagnostics.png` consumed by the manuscript.

### Sensitivity analysis

To probe robustness to network elasticities and Newton damping parameters run

```bash
python sims/run_sensitivity.py --output-dir .
```

This produces `tables/world_welfare_sensitivity.tex` and `figs/policy_sensitivity.png`, comparing first- and second-order tariff responses under ±25% elasticity shifts and alternative damping.

### Distributional estimation

Estimate Stone–Geary parameters from household budgets (real or synthetic fallback) and generate diagnostic Engel curves via

```bash
python sims/make_distributional.py --budget-data data/budgets.csv --output-dir tables --fig-dir figs
```

Outputs: `tables/stone_geary_estimates.tex` and `figs/stone_geary_engel.png`, alongside the canonical copies in `tables/` and `figs/`.

### Macro validation

If you have a `FRED_API_KEY` in the environment the script will pull actual data; otherwise it falls back to a synthetic trend so CI never fails:

```bash
python sims/make_macro_figs.py --start 2010-01-01 --output-dir .
```

The script caches FRED pulls under `data/cache/` by default so repeated runs are instant. Outputs: `figs/macro_validation.png` and `tables/macro_validation.tex`.

## Testing

Run

```bash
python -m pytest
```

The tests cover the GE solver, sparse Leontief routines, Stone–Geary demand, granular convexity, modern econometrics, policy pipeline, and FRED fallbacks.

## Citation

If you use this toolkit, please cite the accompanying paper once posted.
