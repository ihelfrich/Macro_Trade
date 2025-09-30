"""Estimate Stone–Geary parameters and produce distributional outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.common.io import write_fig, write_table
from src.empirics.engel import estimate_sg_from_budgets, natural_sort_labels
from src.empirics.pipeline import synthetic_budget_data


def load_budget_data(path: Path | None, synthetic_sectors: int = 10) -> pd.DataFrame:
    if path and path.exists():
        if path.suffix.lower() in {".csv", ".txt"}:
            return pd.read_csv(path)
        if path.suffix.lower() in {".parquet", ".feather"}:
            return pd.read_parquet(path)
        raise ValueError(f"Unsupported budget data format: {path.suffix}")
    return synthetic_budget_data(sectors=synthetic_sectors)


def build_parameter_table(
    df: pd.DataFrame,
    alpha_by_group: dict[str, np.ndarray],
    gamma_by_group: dict[str, np.ndarray],
    alpha_se: dict[str, np.ndarray] | None = None,
    gamma_se: dict[str, np.ndarray] | None = None,
    goods: list[str] | None = None,
) -> pd.DataFrame:
    goods = goods or natural_sort_labels(df["good"].unique())
    rows: list[dict[str, object]] = []
    for group in sorted(alpha_by_group.keys()):
        alpha = alpha_by_group[group]
        gamma = gamma_by_group[group]
        for idx, (good, a_val, g_val) in enumerate(zip(goods, alpha, gamma)):
            good_latex = good.replace("_", "\\_")
            row = {
                "group": group,
                "good": good_latex,
                "alpha": float(a_val),
                "gamma": float(g_val),
            }
            if alpha_se is not None and gamma_se is not None:
                row["alpha_se"] = float(alpha_se[group][idx])
                row["gamma_se"] = float(gamma_se[group][idx])
            rows.append(row)
    table = pd.DataFrame(rows)
    table = table.rename(columns=lambda c: c.replace("_", "\\_"))
    return table


def plot_engel_curve(df: pd.DataFrame, output_path: Path) -> None:
    goods = natural_sort_labels(df["good"].unique())
    target_good = goods[0]
    fig, ax = plt.subplots(figsize=(7, 4))

    for group, gdf in df[df["good"] == target_good].groupby("group"):
        sub = gdf.sort_values("income")
        sub = sub.assign(share=sub["expenditure"] / sub["income"].clip(lower=1e-6))
        quantiles = np.linspace(0, 1, 10)
        bins = pd.qcut(sub["income"], q=quantiles[1:-1], duplicates="drop")
        grouped = sub.groupby(bins, observed=True)
        mean_income = grouped["income"].mean()
        mean_share = grouped["share"].mean()
        ax.plot(mean_income, mean_share, marker="o", label=group)

    ax.set_xlabel("Income")
    ax.set_ylabel(f"Budget share: {target_good}")
    ax.set_title("Engel curves by income group")
    ax.legend(frameon=False)
    ax.grid(True, linestyle="--", alpha=0.4)
    fig.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_fig(fig, str(output_path))
    plt.close(fig)


def bootstrap_parameters(
    df: pd.DataFrame,
    n_boot: int,
    seed: int,
) -> tuple[
    dict[str, np.ndarray],
    dict[str, np.ndarray],
    np.ndarray,
    np.ndarray,
    list[str],
    list[str],
]:
    """Bootstrap Stone–Geary parameters and retain the full draw history."""

    rng = np.random.default_rng(seed)
    groups = sorted(df["group"].unique())
    goods = natural_sort_labels(df["good"].unique())

    alpha_samples: dict[str, list[np.ndarray]] = {g: [] for g in groups}
    gamma_samples: dict[str, list[np.ndarray]] = {g: [] for g in groups}

    household_col = "household" if "household" in df.columns else None

    for _ in range(n_boot):
        sampled_groups = []
        for group in groups:
            gdf = df[df["group"] == group]
            if household_col:
                households = gdf[household_col].unique()
                draws = rng.choice(households, size=len(households), replace=True)
                sampled = pd.concat(
                    [gdf[gdf[household_col] == hh] for hh in draws],
                    ignore_index=True,
                )
            else:
                sampled = gdf.sample(
                    frac=1.0,
                    replace=True,
                    random_state=rng.integers(1 << 32),
                )
            sampled_groups.append(sampled)

        boot_df = pd.concat(sampled_groups, ignore_index=True)
        alpha_b, gamma_b = estimate_sg_from_budgets(boot_df)
        for group in groups:
            alpha_samples[group].append(np.asarray(alpha_b[group], dtype=float))
            gamma_samples[group].append(np.asarray(gamma_b[group], dtype=float))

    alpha_draws = np.stack(
        [np.vstack(alpha_samples[group]) for group in groups], axis=1
    )
    gamma_draws = np.stack(
        [np.vstack(gamma_samples[group]) for group in groups], axis=1
    )

    alpha_se = {
        group: alpha_draws[:, idx, :].std(axis=0, ddof=1)
        for idx, group in enumerate(groups)
    }
    gamma_se = {
        group: gamma_draws[:, idx, :].std(axis=0, ddof=1)
        for idx, group in enumerate(groups)
    }

    return alpha_se, gamma_se, alpha_draws, gamma_draws, groups, goods


def main() -> None:  # pragma: no cover - CLI entry point
    parser = argparse.ArgumentParser(description="Estimate Stone-Geary parameters")
    parser.add_argument(
        "--budget-data",
        default="data/budgets.csv",
        help=(
            "CSV/Parquet file with budget data (group, income, good, expenditure,"
            " price)."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default="tables",
        help="Directory where parameter tables will be written.",
    )
    parser.add_argument(
        "--fig-dir",
        default="figs",
        help="Directory for diagnostic figures.",
    )
    parser.add_argument(
        "--cache-dir",
        default="data/cache",
        help="Directory for cached bootstrap draws.",
    )
    parser.add_argument(
        "--sector-list",
        default="",
        help="Optional text/CSV file with desired sector labels (one per line).",
    )
    parser.add_argument(
        "--synthetic-sectors",
        type=int,
        default=10,
        help="Number of sectors to generate when using synthetic budget data.",
    )
    parser.add_argument(
        "--bootstrap",
        type=int,
        default=200,
        help="Number of bootstrap draws for standard errors (0 to disable).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="RNG seed for bootstrap resampling.",
    )
    args = parser.parse_args()

    budget_path = Path(args.budget_data)
    df = load_budget_data(budget_path if budget_path.exists() else None, synthetic_sectors=args.synthetic_sectors)
    goods = natural_sort_labels(df["good"].unique())

    sector_list_path = Path(args.sector_list) if args.sector_list else None
    if sector_list_path and sector_list_path.exists():
        sector_labels = _load_sector_labels(sector_list_path)
        if len(sector_labels) == len(goods):
            mapping = {old: new for old, new in zip(goods, sector_labels)}
            df = df.assign(good=df["good"].map(mapping))
            goods = sector_labels
    alpha_by_group, gamma_by_group = estimate_sg_from_budgets(df)

    alpha_se = gamma_se = None
    boot_payload = None
    if args.bootstrap > 0:
        (
            alpha_se,
            gamma_se,
            alpha_draws,
            gamma_draws,
            boot_groups,
            boot_goods,
        ) = bootstrap_parameters(df, args.bootstrap, args.seed)
        boot_payload = {
            "groups": boot_groups,
            "goods": boot_goods,
            "alpha_draws": alpha_draws,
            "gamma_draws": gamma_draws,
        }

    table = build_parameter_table(
        df, alpha_by_group, gamma_by_group, alpha_se, gamma_se, goods
    )
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    table_path = output_dir / "stone_geary_estimates.tex"
    write_table(table, str(table_path))

    fig_dir = Path(args.fig_dir)
    fig_path = fig_dir / "stone_geary_engel.png"
    plot_engel_curve(df, fig_path)

    canonical_table = Path("tables") / "stone_geary_estimates.tex"
    canonical_table.parent.mkdir(parents=True, exist_ok=True)
    write_table(table, str(canonical_table))

    canonical_fig = Path("figs") / "stone_geary_engel.png"
    canonical_fig.parent.mkdir(parents=True, exist_ok=True)
    if fig_path.resolve() != canonical_fig.resolve():
        canonical_fig.write_bytes(fig_path.read_bytes())

    if boot_payload is not None:
        cache_dir = Path(args.cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        np.savez(
            cache_dir / "stone_geary_bootstrap.npz",
            groups=np.array(boot_payload["groups"], dtype="U"),
            goods=np.array(boot_payload["goods"], dtype="U"),
            alpha_draws=boot_payload["alpha_draws"],
            gamma_draws=boot_payload["gamma_draws"],
        )


def _load_sector_labels(path: Path) -> list[str]:
    if path.suffix.lower() in {".csv", ".txt"}:
        values = pd.read_csv(path, header=None).iloc[:, 0].astype(str).tolist()
    else:
        values = Path(path).read_text(encoding="utf-8").splitlines()
    return [label.strip() for label in values if label.strip()]


if __name__ == "__main__":
    main()
