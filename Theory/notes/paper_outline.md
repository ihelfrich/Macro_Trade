
# Paper Rewrite Outline

## Target Structure
1. **Introduction**
   - Motivation: fragmented globalization, reroute vs sever trade tensions.
   - Contributions: theory (three propositions + BF bounds), quantitative GE, empirics, distributional incidence, macro validation.
2. **Environment and Assumptions**
   - Multi-region CES production/consumption; Armington; Stone-Geary households.
   - Assumptions list (A1--A6) referencing theory outline.
3. **Theoretical Results**
   - Prop 1: Reroute ≥ Sever (conditions, equality cases, capacity counterexample).
   - Prop 2: IO amplification bound + second-order error.
   - Prop 3: Granular convexity; BF correction corollary.
4. **Calibration and Data**
   - MRIO source (doc `data/calibration.yaml`, `load_mrio` synthetic fallback); parameter table from `calibration_table`.
   - Stone–Geary groups summary (table via `stone_geary_matrix`).
5. **Quantitative GE**
   - Baseline equilibrium, convergence diagnostics, FO vs SO welfare gap.
   - Policy experiments (tariffs, sanctions, reroute, CBAM, FX) with sensitivity (±25% elasticities, damping).
6. **Empirical Evidence**
   - Staggered adoption event study (dataset from `synthetic_staggered_panel` until real data); Sun–Abraham implementation details.
   - IV diagnostics (dataset from `synthetic_iv_dataset`; highlight F/KP/LIML/AR/over-ID).
7. **Distributional Incidence**
   - Stone–Geary estimation using budget data; EV ratios by income group.
8. **Macro Validation**
   - FRED series (CPI/PPI/IP/10Y) vs model aggregates; figure/table referencing `figs/macro_validation*.png`.
9. **Policy Discussion & Conclusion**
   - Summaries, limitations, future data integration.

## Appendices
- Proofs of Propositions 1–3, BF bounds.
- Additional calibration and sensitivity tables.
- Empirical robustness (placebos, weak-IV cases).
- Data cleaning + replication instructions.

## Action Items
- Populate each section with current synthetic outputs, flag TODOs for real data integration.
- Ensure tables/figures generated via scripts (`sims/run_world_GE.py`, `sims/make_macro_figs.py`).
