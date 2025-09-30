# OECD ICIO SML (2017–2022) Data Notes

## Contents & Coverage
- **Location:** `2017-2022_SML/`, one CSV per year (`{year}_SML.csv`).
- **Scope:** 81 economies (80 individual economies plus the aggregated `ROW`) × 50 industries, following the OECD ICIO SML industry-by-industry layout.
- **Years:** 2017–2022 inclusive; files share an identical schema with 4 053 rows × 4 538 columns.
- **Units:** Current-price millions of US dollars at basic prices (per OECD ICIO documentation).

## Table Layout
- **Row index (`V1`):** Sector identifiers in the form `CCC_SSS`, where `CCC` is the 3-letter economy code and `SSS` is one of 50 industry groupings (`A01`, `C10T12`, `J62_63`, …). Rows end with two aggregates: `VA` (value added) and `OUT` (gross output).
- **Intermediate-demand block:** The first 4 050 data columns mirror the industry rows—one column per economy-sector pair—containing inter-industry flows.
- **Final-demand block:** For each economy there are six columns: `HFCE`, `NPISH`, `GGFC`, `GFCF`, `INVNT`, `DPABR` (household consumption, non-profits, government consumption, capital formation, inventory changes, and direct purchases abroad). These occupy 486 columns (81 economies × 6 uses).
- **Terminal column (`OUT`):** Column totals for each producing sector (equals intermediate sales + final demand + exports).

## How It Fits the Project
These matrices provide the real MRIO backbone the project has been waiting for. Each file already contains everything needed to swap out the synthetic 3×10 benchmark in `src/data/mrio_loader.py`:

1. **Choose a base year.** Load `Y = pd.read_csv("2017-2022_SML/2021_SML.csv")`, or expose the year as a loader argument so counterfactuals can span 2017–2022.
2. **Extract industry sets.** Build ordered lists of economies (prefixes) and industries (suffixes) by parsing `Y['V1']`.
3. **Intermediate matrix (`Z`).** Slice the 4 050×4 050 block of inter-industry flows and convert to sparse CSR; divide each column by the corresponding gross output from the `OUT` row to obtain the technical-coefficient matrix `A`.
4. **Value added (`VA`).** Use the `VA` row restricted to the 4 050 industry columns; normalise by gross output for Domar weights or keep the level vector for income accounting.
5. **Final demand (`F`).** Stack the six final-demand columns per economy; you can either keep the full 6-way breakdown or aggregate to a single vector per economy when computing total absorption.
6. **Outputs (`x`).** Take the `OUT` row over industry columns—this is the gross output vector needed for balancing and welfare calculations.
7. **Metadata.** Store the ordered economy and sector labels so the policy engine can align wedges/tariffs to the expanded economy set.

Once these pieces are assembled, update `data/mrio_config.yaml` to point to the processed OECD-backed artefacts instead of the synthetic fallback. The existing calibration scaffolding already supports per-sector elasticities; you will mainly need to (i) provide a 50-sector elasticity profile and (ii) optionally aggregate to the project’s smaller sectoring before feeding into simulations.

## Practical Considerations
- **Size:** Each CSV is ~140 MB uncompressed; convert to `.npz`/Feather for faster IO inside CI.
- **Rest of World:** `ROW_*` sectors act as a residual economy. Decide whether to keep it or treat it as exogenous when computing Domar weights.
- **Consistency:** Industry and final-demand codes are stable across years, enabling panel analyses or multi-year calibration.
- **Cleaning:** There are no headers besides `V1`; ensure downstream code drops `VA`/`OUT` rows and the terminal `OUT` column before forming the coefficient matrix.
- **Diagnostics:** After constructing `A`, verify that `(I - A)` is invertible (spectral radius < 1) and that `Z + F` reconstructs the gross-output vector for a handful of sectors as a balance check.

With this mapping in place, the project can transition from the toy 3×10 MRIO to an OECD-calibrated, 81×50 network, unlocking external validity for the GE, welfare, and policy modules.
