# Econometrica-Grade Expansion Blueprint

## North Star
Produce a single Econometrica-calibre paper on "Fragmented Globalization" that bundles:
- Formal theory (multi-region, multi-sector CES with IO links, Armington trade, Stone–Geary demand) featuring novel propositions and proofs.
- Quantitative GE calibrated on a real MRIO (OECD-ICIO/WIOD) or a well-documented synthetic fallback, including nonlinear solves, FO/SO welfare comparisons, and sensitivity analysis.
- Credible empirics: Sun–Abraham staggered adoption design with modern inference, plus IV diagnostics (F_first, KP rk, LIML, AR p & CI, over-ID tests).
- Distributional analysis: Stone–Geary estimation across income groups, equivalent-variation incidence for policy scenarios.
- Macro validation using live FRED data; replication-ready code (tests, CI, scripts).

## Pillars & Deliverables

### A. Theory
1. **Environment setup**
   - Explicit primitives: countries, sectors, consumers (Armington CES across origins), firms with IO matrix A, iceberg trade costs, Stone–Geary final demand.
   - Assumptions (e.g., ρ(A) < 1, elasticity bounds, capacity constraints).
2. **Propositions**
   - **Prop 1 (Reroute ≥ Sever)**: Welfare loss under rerouting ≤ severing under stated capacity conditions; characterize equality cases; provide counterexample when capacity binds.
   - **Prop 2 (IO amplification bound)**: Bound welfare-loss slope by spectral radius/elasticities; include Neumann-series truncation error determining second-order gap.
   - **Prop 3 (Granular convexity)**: Show convexity of welfare loss in exposure concentration with small shocks and SG demand; identify curvature term.
   - Baqaee–Farhi FO vs SO error bound with computable curvature scalar.
3. **Appendix proofs**: Formal proofs, lemmas, assumptions organized for Econometrica tone.

### B. Quantitative GE
1. **Data sourcing**
   - Search `data/` for MRIO (e.g., OECD-ICIO, WIOD). If absent, document deterministic synthetic (3–5 countries × 10 sectors). Placeholders for swapping to real data.
2. **Calibration**
   - Table of elasticities, parameters (Armington, substitution, Stone–Geary γ, α). Cite literature.
3. **Computation**
   - Extend `solve_ge` with diagnostics; compute Domar weights; build network Hessian.
   - Produce FO vs SO welfare metrics; report convergence stats.
4. **Policy experiments**
   - Implement tariffs, sanctions, reroute capacities, CBAM, FX toggle via JSON/YAML.
   - Outputs: `tables/world_welfare.tex`, `tables/distributional_incidence.tex`, `figs/policy_scenarios.png`, `figs/map_global_welfare.png`.
5. **Sensitivity**
   - ±25% elasticity scenarios, alternate damping, curvature toggles; tabulate outcomes.

### C. Empirics
1. **Event study**
   - Build or source staggered adoption dataset (real MRIO events or simulated). Implement Sun–Abraham estimator with never/late controls, joint pretrend chi-square, placebo windows.
   - Output dynamic coefficients plot with CI, pretrend p-value.
2. **IV diagnostics**
   - Expand `iv2sls_cluster` with F_first, KP rk, LIML, AR p & CI, over-ID test.
   - Provide strong vs weak instrument case studies; table summarizing diagnostics.
   - Document identification assumptions and datasets.

### D. Distributional Incidence
1. **Stone–Geary estimation**
   - Use household budget data (real or simulated). Estimate α, γ by income group via NLS/OLS with bootstrap CIs.
   - Report table with estimates + standard errors.
2. **Welfare incidence**
   - Compute equivalent-variation ratios per group for each policy scenario. Analyze variance, luxury-good channel.

### E. Macro Validation
1. **FRED integration**
   - Use available `FRED_API_KEY` to fetch CPI, PPI, IP, 10Y yields.
   - Generate `figs/macro_validation_*.png`, `tables/macro_validation.tex` with summary stats.
2. **Narrative**
   - Compare model aggregates vs FRED series; discuss alignment/mismatch.

### F. Documentation & CI
1. **Paper rewrite**
   - Econometrica-style structure: Introduction, Model, Equilibrium Analysis, Quantitative Calibration, Empirics, Policy Counterfactuals, Macro Validation, Conclusion, Appendices.
   - Insert propositions, tables, figures; ensure paths valid.
   - Update `paper/refs.bib` (EK 2002, Melitz 2003, ACR 2012, Caliendo–Parro 2015, Baqaee–Farhi 2019, Sun–Abraham 2021, Cameron–Gelbach–Miller 2011, MRIO references, etc.).
2. **README overhaul**
   - Document data requirements, commands, MRIO filenames, FRED usage, interpretation guidance.
3. **Replication**
   - CI via `bash ci/run_all.sh`: run pytest, simulations, macro scripts, build paper.
   - Ensure outputs reproducible, tests cover new modules.

## Work Plan (Iterative)
1. **Audit & data inventory**: Confirm available datasets, current code state, test coverage.
2. **Theory drafting**: Formalize model, draft propositions + proof outlines.
3. **GE calibration pipeline**: Implement data loader, parameter table, baseline solve.
4. **Policy simulations**: Configure scenarios, run baseline + sensitivities, gather outputs.
5. **Empirical module**: Build event-study dataset, run Sun–Abraham, expand IV module, produce tables/plots.
6. **Distributional block**: Estimate Stone–Geary, compute welfare incidence.
7. **Macro validation**: Execute FRED pulls, generate figures/tables, interpret results.
8. **Compose manuscript**: Integrate results, finalize proofs in appendices, align references.
9. **Documentation & testing**: Update README, ensure CI pipeline, verify reproducibility.
10. **Final polish**: Check figures (grayscale friendly), tables (threeparttable), typography, ensure `paper/main.pdf` builds cleanly.

## Outstanding Questions/Assumptions
- Availability of real MRIO and household budget data in repo or via download (may need placeholders + TODO notes).
- Whether to simulate staggered adoption if real policy shocks not readily accessible.
- Time budget for numerical robustness (bootstraps, multiple calibrations).

Use this blueprint to track progress; update as components are completed or requirements change.


## Repository Audit (2025-09-26)
- **Data**: `data/` currently holds only `mrio_config.yaml`; no real MRIO or household budget datasets checked in. Synthetic MRIO loader remains default until real data provided.
- **Scripts**: Policy simulator (`sims/run_world_GE.py`) and macro validation (`sims/make_macro_figs.py`) exist; tests rely on synthetic outputs.
- **Empirics**: No real staggered-treatment or IV datasets present; will need simulated panels or documented external sources.
- **Distributional**: No household budget microdata available; Stone–Geary estimation must use simulated data pending real inputs.
- **CI**: `python3.12 -m pytest` passes (29 tests). `ci/run_all.sh` orchestrates tests+sims+paper with synthetic fallback.


## Empirical Scaffolding (2025-09-26)
- Added `src/empirics/pipeline.py` generating synthetic staggered panels, IV datasets, and Stone-Geary budget microdata for future estimation.
- Created tests (`tests/test_pipeline.py`) to guarantee shapes and variance properties; will swap in real data loaders later.
- Introduced `src/trade/calibration.py` with YAML-driven elasticities (`data/calibration.yaml`) and coverage test (`tests/test_calibration.py`).


## Calibration & Policy Integration (2025-09-26)
- `src/policy/simulate.py` now ingests `data/calibration.yaml` via the new `load_calibration` helper, building sector-specific network elasticities for the Hessian and populating Stone–Geary groups (with fallback to synthetic defaults).
- Added `_network_elasticities_vector` and `_stone_geary_groups` utilities so policy simulations respect calibration inputs across countries/sectors.
- Extended package exports/tests remain green (`tests/test_policy.py`).


## Calibration Tables (2025-09-26)
- Added `sims/make_calibration_tables.py` with CLI + helper to emit `tables/calibration_params.tex` and `tables/stone_geary_groups.tex` using the calibration YAML and MRIO sectors.
- Strings summarise Stone–Geary vectors; falls back to synthetic groups if calibration file lacks entries.
- Automated test `tests/test_calibration_tables.py` verifies table generation.


## CI pipeline update (2025-09-26)
- Added calibration-table generation to `ci/run_all.sh` so the replication script now emits parameter summaries alongside existing outputs.
- Verified `python3 sims/make_calibration_tables.py` runs under `PYTHONPATH=.` and extended full pytest run (`34 passed`).


## Policy pipeline calibration hook (2025-09-26)
- `sims/run_world_GE.py` accepts `--calibration` flag; `run_policy_scenarios` forwards the path, defaulting to `data/calibration.yaml` unless overridden.
- Manual smoke test: `PYTHONPATH=. python3 sims/run_world_GE.py --calibration data/calibration.yaml ...` writes policy outputs under `/tmp/gee`.
- Targeted tests (`tests/test_policy.py`, `tests/test_calibration_tables.py`) rerun cleanly.


## Paper skeleton upgrade (2025-09-26)
- Rewrote `paper/main.tex` into Econometrica-style structure: environment, assumptions (A1--A6), propositions, calibration tables, policy/empirical/macro sections, and appendix placeholders.
- Added LaTeX assets (placeholder tables/figures) plus threeparttable/siunitx formatting; updated `make_calibration_tables.py` and CLI hooks accordingly.
- Verified TeX build with `make paper` (after generating calibration + placeholder outputs).


## Empirical integration (2025-09-27)
- Implemented `sims/make_empirics.py` to generate Sun–Abraham event-study tables/plots and clustered IV diagnostics with synthetic fallbacks; added direct test coverage.
- Updated `Makefile` and `ci/run_all.sh` to run simulations/scripts under `PYTHONPATH=.` ensuring reusable module imports inside CI.
- Expanded the manuscript's empirical section with the new figures/tables and notes; LaTeX now compiles after the scripts run (only presentation overfull warnings remain).
- Refreshed the README with instructions for the empirical generator and clarified the CI pipeline ordering.

## Macro validation caching (2025-09-27)
- Extended `sims/make_macro_figs.py` with on-disk caching of FRED pulls (`data/cache/`) and a helper for tests; enhanced tests to cover cached fallbacks.
- Generated live FRED series using the repository API key, updating `figs/macro_validation.png` and `tables/macro_validation.tex`.


## Distributional estimation (2025-09-27)
- Added `sims/make_distributional.py` to estimate Stone–Geary parameters from budget data (real or synthetic) and emit `tables/stone_geary_estimates.tex` plus `figs/stone_geary_engel.png`.
- Introduced regression tests (`tests/test_distributional.py`) to ensure alphas sum to one, gammas remain non-negative, and the script writes the expected artefacts.
- Updated the distributional section of the manuscript with the new table/figure and narrative discussing luxury-good channels.


## Integration strategy (next steps)

### Phase 1 — Theory proofs and sensitivities (target: Week 1)
- Draft rigorous proofs for Propositions~1–3 and the Baqaee–Farhi bound in `paper/appendix_proofs.tex`, cross-reference in the main text.
- Extend GE solver coverage: add regression tests (e.g. `tests/test_sensitivity.py`) that run `solve_ge` under ±25% elasticity shocks and alternative damping.
- Implement sensitivity scripts (`sims/run_sensitivity.py`) that write `tables/world_welfare_sensitivity.tex` and `figs/policy_sensitivity.png`; wire into `ci/run_all.sh` after the baseline simulations.
- Update blueprint status once proofs compile cleanly and CI covers the new scenarios.

### Phase 2 — Distributional estimation upgrade (target: Week 2)
- Source or simulate richer household budget data; implement Stone–Geary estimation in `src/empirics/engel.py` with bootstrapped standard errors.
- Add unit tests validating monotonic luxury shares and confidence interval coverage.
- Regenerate `tables/stone_geary_groups.tex` from estimated parameters; refresh manuscript Section~"Distributional Incidence" with the new estimates and uncertainty discussion.

### Phase 3 — Macro validation with live data (target: Week 3)
- Enhance `sims/make_macro_figs.py` to cache FRED pulls in `data/cache/` while respecting rate limits; add tests for the caching logic.
- Modify `ci/run_all.sh` to use live data when `FRED_API_KEY` is available, otherwise fall back to cached series.
- Expand the macro validation narrative in the paper, contrasting model aggregates with the fetched series.

### Phase 4 — Documentation & polish (rolling)
- Document new scripts and data expectations in `README.md` and `project_blueprint.md` after each phase.
- Address LaTeX overfull boxes (narrower tables or `\small` environments) once final numbers are in place.
- Run `bash ci/run_all.sh` before handoff to ensure the full integration remains reproducible.
