"""Generate empirical tables and figures for event studies and IV diagnostics."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.common.io import write_fig, write_table
from src.empirics.pipeline import (
    StaggeredConfig,
    synthetic_iv_dataset,
    synthetic_staggered_panel,
)
from src.empirics.utils import iv2sls_cluster, sun_abraham


def generate_event_study_outputs(output_dir: Path, cfg: StaggeredConfig):
    panel = synthetic_staggered_panel(cfg)
    results = sun_abraham(panel)
    table = results['table'].copy()
    if table.empty:
        table = pd.DataFrame({'rel_time': [], 'beta': [], 'se': [], 'ci_low': [], 'ci_high': []})
        pretrend_df = pd.DataFrame({'stat': ['pretrend_p'], 'value': [np.nan]})
    else:
        table['ci_low'] = table['beta'] - 1.96 * table['se']
        table['ci_high'] = table['beta'] + 1.96 * table['se']
        pretrend_df = pd.DataFrame({
            'stat': ['pretrend_p'],
            'value': [results['pretrend_p']],
        })

    table_display = table.rename(
        columns={
            'rel_time': 'Event time',
            'beta': 'Beta',
            'se': 'SE',
            'ci_low': 'CI (low)',
            'ci_high': 'CI (high)',
        }
    )
    write_table(table_display, str(output_dir / 'tables' / 'es_main.tex'))

    pretrend_display = pretrend_df.copy()
    pretrend_display['stat'] = 'Pretrend p-value'
    pretrend_display = pretrend_display.rename(columns={'stat': 'Statistic', 'value': 'Value'})
    write_table(pretrend_display, str(output_dir / 'tables' / 'es_pretrend.tex'))

    if table.empty:
        return table, pretrend_df

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axhline(0.0, color='black', linewidth=0.8)
    ax.plot(table['rel_time'], table['beta'], marker='o', label='Estimated effect')
    ax.fill_between(table['rel_time'], table['ci_low'], table['ci_high'], alpha=0.25, label='95% CI')
    ax.set_xlabel('Event time (quarters)')
    ax.set_ylabel('Coefficient')
    ax.set_title('Sun–Abraham event-study estimates')
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.4)
    ax.legend(frameon=False)
    fig.tight_layout()
    write_fig(fig, str(output_dir / 'figs' / 'event_study.png'))
    plt.close(fig)

    return table, pretrend_df


def generate_iv_outputs(output_dir: Path, n: int = 400, seed: int = 0):
    strong = synthetic_iv_dataset(n=n, strength=0.8, seed=seed)
    weak = synthetic_iv_dataset(n=n, strength=0.05, seed=seed + 7)

    strong_res = iv2sls_cluster(strong['y'], strong['x'], strong['Z'], strong['cluster'])
    weak_res = iv2sls_cluster(weak['y'], weak['x'], weak['Z'], weak['cluster'])

    rows = []
    for label, res in [('Strong', strong_res), ('Weak', weak_res)]:
        beta = float(res['beta'][1]) if res['beta'].size > 1 else float(res['beta'][0])
        se = float(res['se'][1]) if res['se'].size > 1 else float(res['se'][0])
        ar_ci = res['AR_CI'] if isinstance(res['AR_CI'], (tuple, list)) else (np.nan, np.nan)
        rows.append(
            {
                'scenario': label,
                'beta': beta,
                'se': se,
                'F_first': res['F_first'],
                'KP_rk': res['KP_rk'],
                'LIML': float(res['LIML'][1]) if res['LIML'].size > 1 else float(res['LIML'][0]),
                'AR_p': res['AR_p'],
                'AR_low': ar_ci[0],
                'AR_high': ar_ci[1],
            }
        )

    table = pd.DataFrame(rows)
    table_display = table.rename(
        columns={
            'scenario': 'Scenario',
            'beta': 'Beta',
            'se': 'SE',
            'F_first': 'First-stage F',
            'KP_rk': 'KP rk',
            'LIML': 'LIML',
            'AR_p': 'AR p-val',
            'AR_low': 'AR CI low',
            'AR_high': 'AR CI high',
        }
    )
    write_table(table_display, str(output_dir / 'tables' / 'iv_main.tex'))

    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(len(rows))
    width = 0.35
    ax.bar(x - width / 2, table['F_first'], width=width, label='First-stage F')
    ax.bar(x + width / 2, table['KP_rk'], width=width, label='Kleibergen-Paap rk')
    ax.set_xticks(x)
    ax.set_xticklabels(table['scenario'])
    ax.set_ylabel('Statistic')
    ax.set_title('IV strength diagnostics')
    ax.legend(frameon=False)
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.4)
    fig.tight_layout()
    write_fig(fig, str(output_dir / 'figs' / 'iv_diagnostics.png'))
    plt.close(fig)

    return table


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate empirical outputs for the paper.')
    parser.add_argument('--output-dir', default='.', help='Directory for tables/ and figs/.')
    parser.add_argument('--units', type=int, default=48, help='Number of panel units in synthetic event study.')
    parser.add_argument('--periods', type=int, default=16, help='Number of time periods.')
    parser.add_argument('--event-effect', type=float, default=1.0, help='Treatment effect size.')
    parser.add_argument('--seed', type=int, default=0, help='Random seed baseline.')
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    cfg = StaggeredConfig(units=args.units, periods=args.periods, effect=args.event_effect, seed=args.seed)
    generate_event_study_outputs(output_dir, cfg)
    generate_iv_outputs(output_dir, n=400, seed=args.seed)


if __name__ == '__main__':  # pragma: no cover - CLI entry point
    main()
