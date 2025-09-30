"""Policy counterfactual pipeline tying MRIO, GE, and welfare analytics."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
from scipy.sparse import csr_matrix

from src.common.io import write_fig, write_table
from src.data.mrio_loader import load_mrio
from src.trade.ge import solve_ge
from src.trade.welfare import build_network_hessian, welfare_first_order, welfare_second_order
from src.trade.nonhomothetic import welfare_ev_ratio
from src.trade.calibration import CalibrationConfig, load_calibration


@dataclass
class ScenarioResult:
    name: str
    description: str
    fo_global: float
    so_global: float
    country_metrics: Dict[str, Dict[str, float]]
    ev_groups: Dict[str, Dict[str, float]]
    dlog_p: np.ndarray
    prices: np.ndarray


class MRIOIndexer:
    def __init__(self, countries: Sequence[str], sectors: Sequence[str]):
        self.countries = list(countries)
        self.sectors = list(sectors)
        self.n_sectors = len(sectors)

    def idx(self, country: str, sector: str) -> int:
        if country not in self.countries:
            raise KeyError(f"Unknown country '{country}'")
        if sector not in self.sectors:
            raise KeyError(f"Unknown sector '{sector}'")
        return self.countries.index(country) * self.n_sectors + self.sectors.index(sector)

    def country_slice(self, country: str) -> List[int]:
        if country not in self.countries:
            raise KeyError(f"Unknown country '{country}'")
        base = self.countries.index(country) * self.n_sectors
        return list(range(base, base + self.n_sectors))

    def all_indices(self) -> range:
        return range(len(self.countries) * self.n_sectors)


def run_policy_scenarios(
    policy_config_path: str,
    mrio_config_path: str = "data/mrio_config.yaml",
    output_dir: str = ".",
    calibration_path: str | None = None,
    calibration: CalibrationConfig | None = None,
    solver_kwargs: Dict[str, object] | None = None,
    write_outputs: bool = True,
) -> List[ScenarioResult]:
    policy_cfg = _load_json(policy_config_path)
    mrio_cfg = _load_yaml(mrio_config_path)
    mrio_kwargs = mrio_cfg.get('mrio', {})

    A_csr, VA, Y, sectors, countries = load_mrio(**mrio_kwargs)
    if calibration is None:
        calibration_file = calibration_path or mrio_cfg.get('calibration_path', 'data/calibration.yaml')
        calibration = load_calibration(calibration_file)
    indexer = MRIOIndexer(countries, sectors)
    K = len(countries) * len(sectors)

    p0 = np.ones(K)
    baseline_sol = solve_ge(
        p0,
        np.zeros(K),
        A_csr,
        sigma_origin=4.0,
        linear=False,
        **(solver_kwargs or {}),
    )
    domar = baseline_sol['domar']
    network_eps = _network_elasticities_vector(calibration, countries, sectors)
    H = build_network_hessian(A_csr, network_eps)
    p_baseline = baseline_sol['p']

    scenarios = policy_cfg.get('scenarios', [])
    if not scenarios or scenarios[0].get('policies'):
        scenarios = [{'name': 'Baseline', 'description': 'No policy change', 'policies': {}}] + scenarios

    sg_groups = _stone_geary_groups(calibration, countries, sectors)
    _attach_sg_bootstrap(sg_groups, calibration, countries, sectors)

    results: List[ScenarioResult] = []
    for scenario in scenarios:
        name = scenario.get('name', 'Scenario')
        desc = scenario.get('description', '')
        policies = scenario.get('policies', {})

        if policies:
            A_mod, wedges = _apply_policies(A_csr, policies, indexer)
            A_for_solve = csr_matrix(A_mod)
            wedges_vec = wedges
        else:
            A_for_solve = A_csr
            wedges_vec = np.zeros(K)

        sol = solve_ge(
            p0,
            wedges_vec,
            A_for_solve,
            sigma_origin=4.0,
            linear=False,
            **(solver_kwargs or {}),
        )
        dlog_p = np.log(sol['p'] / p_baseline)
        fo = welfare_first_order(dlog_p, domar)
        so = welfare_second_order(dlog_p, domar, H)
        country_metrics = _country_welfare(domar, H, dlog_p, countries, indexer)
        ev_ratios = _group_ev_ratios(sg_groups, p_baseline, sol['p'])

        results.append(
            ScenarioResult(
                name=name,
                description=desc,
                fo_global=fo,
                so_global=so,
                country_metrics=country_metrics,
                ev_groups=ev_ratios,
                dlog_p=dlog_p,
                prices=sol['p'],
            )
        )

    if write_outputs:
        _emit_outputs(results, countries, output_dir)
    return results


# ---------------------------------------------------------------------------
# Policy transforms
# ---------------------------------------------------------------------------


def _apply_policies(A_csr: csr_matrix, policies: Dict, indexer: MRIOIndexer):
    A = A_csr.toarray()
    K = A.shape[0]
    wedges = np.zeros(K)

    for tariff in policies.get('tariffs', []):
        dest = tariff['dest']
        sector = tariff['sector']
        tau = tariff.get('tau', 0.0)
        idx = indexer.idx(dest, sector)
        wedges[idx] += np.log1p(tau)

    for fx in policies.get('fx', []):
        country = fx['country']
        shock = fx.get('change', 0.0)
        for idx in indexer.country_slice(country):
            wedges[idx] += shock

    for cbam in policies.get('cbam', []):
        rate = cbam.get('rate', 0.0)
        sector = cbam['sector']
        intensity = cbam.get('intensity', {})
        for country, value in intensity.items():
            idx = indexer.idx(country, sector)
            wedges[idx] += rate * value

    for sanction in policies.get('sanctions', []):
        origin = sanction['origin']
        dest = sanction['dest']
        sectors = sanction.get('sectors') or indexer.sectors
        dest_sectors = sanction.get('dest_sectors') or indexer.sectors
        origin_indices = [indexer.idx(origin, s) for s in sectors]
        dest_indices = [indexer.idx(dest, s) for s in dest_sectors]
        for r in origin_indices:
            for c in dest_indices:
                A[r, c] = 0.0

    for reroute in policies.get('reroute', []):
        origin = reroute['origin']
        dest = reroute['dest']
        multiplier = reroute.get('multiplier', 1.0)
        sectors = reroute.get('sectors') or indexer.sectors
        dest_sectors = reroute.get('dest_sectors') or indexer.sectors
        for s in sectors:
            r = indexer.idx(origin, s)
            for ds in dest_sectors:
                c = indexer.idx(dest, ds)
                A[r, c] *= multiplier

    return A, wedges


# ---------------------------------------------------------------------------
# Welfare accounting helpers
# ---------------------------------------------------------------------------


def _country_welfare(domar, H, dlog_p, countries, indexer):
    metrics = {}
    for country in countries:
        idxs = indexer.country_slice(country)
        fo = -float(domar[idxs] @ dlog_p[idxs])
        quad = float(dlog_p[idxs] @ (H[np.ix_(idxs, indexer.all_indices())] @ dlog_p))
        so = fo - 0.5 * quad
        metrics[country] = {'fo': fo, 'so': so}
    return metrics


def _network_elasticities_vector(calibration, countries, sectors):
    sector_eps = np.asarray([calibration.epsilon_for(sector) for sector in sectors], dtype=float)
    return np.tile(sector_eps, len(countries))


def _stone_geary_groups(calibration, countries, sectors):
    if calibration.groups:
        try:
            return [_expand_group(g, countries, sectors) for g in calibration.groups]
        except ValueError:
            pass  # fall back to synthetic default
    return _synthetic_groups(len(countries), len(sectors))


def _expand_group(group, countries, sectors):
    n_c = len(countries)
    n_s = len(sectors)
    target = n_c * n_s

    def _expand(vec):
        if vec.size == target:
            return vec.astype(float)
        if vec.size == n_s:
            return np.tile(vec, n_c).astype(float)
        raise ValueError("Stone-Geary parameters must match sectors or country-sector dimension")

    alpha = _expand(group.alpha)
    gamma = _expand(group.gamma)
    alpha = alpha / alpha.sum() if alpha.sum() > 0 else alpha
    return {
        'name': group.name,
        'income': group.income,
        'alpha': alpha,
        'gamma': gamma,
    }


def _synthetic_groups(n_countries: int, n_sectors: int):
    K = n_countries * n_sectors
    base_gamma = np.full(K, 0.002)
    base_alpha = np.full(K, 1.0 / K)
    gradients = [np.linspace(0.8, 1.2, K), np.linspace(1.0, 1.0, K), np.linspace(1.2, 0.8, K)]
    incomes = [150.0, 220.0, 320.0]
    groups = []
    for name, income, grad in zip(['Low', 'Middle', 'High'], incomes, gradients):
        alpha = base_alpha * grad
        alpha = alpha / alpha.sum()
        groups.append({'name': name, 'income': income, 'alpha': alpha, 'gamma': base_gamma})
    return groups


def _attach_sg_bootstrap(groups, calibration, countries, sectors):
    payload = _load_sg_bootstrap_file(calibration)
    if payload is None:
        return

    goods = payload['goods']
    goods_index = {good: idx for idx, good in enumerate(goods)}
    try:
        sector_positions = [goods_index[sector] for sector in sectors]
    except KeyError:
        # Goods mismatch; skip bootstrap attachment.
        return

    group_lookup = {name: idx for idx, name in enumerate(payload['groups'])}
    alpha_draws = payload['alpha_draws']
    gamma_draws = payload['gamma_draws']
    n_countries = len(countries)
    n_sectors = len(sectors)

    for group in groups:
        g_idx = group_lookup.get(group['name'])
        if g_idx is None:
            continue
        draws_alpha = alpha_draws[:, g_idx, :][:, sector_positions]
        draws_gamma = gamma_draws[:, g_idx, :][:, sector_positions]
        if draws_alpha.size == 0 or draws_gamma.size == 0:
            continue
        draws_alpha = np.tile(draws_alpha[:, None, :], (1, n_countries, 1)).reshape(draws_alpha.shape[0], n_countries * n_sectors)
        draws_gamma = np.tile(draws_gamma[:, None, :], (1, n_countries, 1)).reshape(draws_gamma.shape[0], n_countries * n_sectors)
        draws_alpha = draws_alpha / draws_alpha.sum(axis=1, keepdims=True)
        draws_gamma = draws_gamma / n_countries
        target_gamma = np.sum(group['gamma'])
        draw_sums = draws_gamma.sum(axis=1, keepdims=True)
        with np.errstate(divide='ignore', invalid='ignore'):
            draws_gamma = np.where(draw_sums > 0, draws_gamma * (target_gamma / draw_sums), draws_gamma)
        group['alpha_draws'] = draws_alpha
        group['gamma_draws'] = draws_gamma


def _load_sg_bootstrap_file(calibration):
    candidates = []
    meta_path = calibration.metadata.get('stone_geary_bootstrap') if calibration.metadata else None
    if meta_path:
        candidates.append(Path(meta_path))
    candidates.append(Path('data') / 'cache' / 'stone_geary_bootstrap.npz')

    for candidate in candidates:
        candidate = Path(candidate)
        if not candidate.exists():
            continue
        with np.load(candidate, allow_pickle=False) as data:
            return {
                'groups': [str(x) for x in data['groups']],
                'goods': [str(x) for x in data['goods']],
                'alpha_draws': data['alpha_draws'],
                'gamma_draws': data['gamma_draws'],
            }
    return None


def _group_ev_ratios(groups, p0, p1):
    y0 = np.array([g['income'] for g in groups], dtype=float)
    alpha = np.vstack([g['alpha'] for g in groups])
    gamma = np.vstack([g['gamma'] for g in groups])
    ev = welfare_ev_ratio(y0, p0, p1, alpha, gamma)

    summaries: Dict[str, Dict[str, float]] = {}
    for idx, group in enumerate(groups):
        metrics: Dict[str, float] = {'ev_ratio': float(ev[idx])}
        draws_alpha = group.get('alpha_draws')
        draws_gamma = group.get('gamma_draws')
        if draws_alpha is not None and draws_gamma is not None:
            try:
                y_draw = np.full(draws_alpha.shape[0], group['income'], dtype=float)
                ev_draws = welfare_ev_ratio(y_draw, p0, p1, draws_alpha, draws_gamma)
                if ev_draws.size > 1:
                    metrics['ev_se'] = float(np.std(ev_draws, ddof=1))
                    metrics['ev_p05'] = float(np.quantile(ev_draws, 0.05))
                    metrics['ev_p95'] = float(np.quantile(ev_draws, 0.95))
                else:
                    metrics['ev_se'] = 0.0
            except ValueError:
                # Dimension mismatch on bootstrap draws; skip uncertainty.
                pass
        summaries[group['name']] = metrics
    return summaries


# ---------------------------------------------------------------------------
# Output construction
# ---------------------------------------------------------------------------


def _emit_outputs(results: List[ScenarioResult], countries: Sequence[str], output_dir: str):
    rows = []
    for res in results:
        rows.append({'scenario': res.name, 'location': 'Global', 'fo_pct': res.fo_global * 100, 'so_pct': res.so_global * 100})
        for country in countries:
            cm = res.country_metrics[country]
            rows.append({'scenario': res.name, 'location': country, 'fo_pct': cm['fo'] * 100, 'so_pct': cm['so'] * 100})
    table_world = pd.DataFrame(rows)
    world_path = Path(output_dir) / 'tables'
    world_path.mkdir(parents=True, exist_ok=True)
    full_csv = world_path / 'world_welfare_full.csv'
    table_world.to_csv(full_csv, index=False)

    summary = _summarise_world_welfare(table_world)
    write_table(summary, str(world_path / 'world_welfare.tex'))

    dist_rows = []
    for res in results:
        for group, metrics in res.ev_groups.items():
            row = {
                'scenario': res.name,
                'group': group,
                'ev_ratio': metrics.get('ev_ratio', float('nan')),
            }
            if 'ev_se' in metrics:
                row['ev_se'] = metrics['ev_se']
            if 'ev_p05' in metrics:
                row['ev_p05'] = metrics['ev_p05']
            if 'ev_p95' in metrics:
                row['ev_p95'] = metrics['ev_p95']
            dist_rows.append(row)
    table_dist = pd.DataFrame(dist_rows)
    write_table(table_dist, str(Path(output_dir) / 'tables' / 'distributional_incidence.tex'))

    _plot_policy_scenarios(results, output_dir)
    _plot_country_incidence(results, countries, output_dir)


def _summarise_world_welfare(table: pd.DataFrame, top_n: int = 12) -> pd.DataFrame:
    summary_rows = []
    for scenario, block in table.groupby('scenario', sort=False):
        block = block.copy()
        global_row = block[block['location'] == 'Global']
        if not global_row.empty:
            summary_rows.append(global_row.iloc[0].to_dict())
        remainder = block[block['location'] != 'Global']
        if not remainder.empty:
            remainder = remainder.assign(abs_so=remainder['so_pct'].abs())
            top = remainder.nlargest(top_n, 'abs_so').drop(columns='abs_so')
            summary_rows.extend(top.to_dict('records'))
    return pd.DataFrame(summary_rows)


def _plot_policy_scenarios(results: List[ScenarioResult], output_dir: str):
    if len(results) <= 1:
        return
    scenarios = [r.name for r in results[1:]]
    fo = [r.fo_global * 100 for r in results[1:]]
    so = [r.so_global * 100 for r in results[1:]]
    x = np.arange(len(scenarios))
    width = 0.35
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(x - width / 2, fo, width=width, label='First order')
    ax.bar(x + width / 2, so, width=width, label='Second order')
    ax.axhline(0, color='black', linewidth=0.75)
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, rotation=15, ha='right')
    ax.set_ylabel('Welfare change (percent)')
    ax.set_title('Policy scenarios: global welfare')
    ax.legend()
    fig.tight_layout()
    write_fig(fig, str(Path(output_dir) / 'figs' / 'policy_scenarios.png'))
    plt.close(fig)


def _plot_country_incidence(results: List[ScenarioResult], countries: Sequence[str], output_dir: str):
    if len(results) < 2:
        return
    scenario = results[-1]
    so = [scenario.country_metrics[c]['so'] * 100 for c in countries]
    fig, ax = plt.subplots(figsize=(6, 4))
    order = np.argsort(so)
    ordered_countries = [countries[i] for i in order]
    ordered_so = [so[i] for i in order]
    ax.barh(ordered_countries, ordered_so)
    ax.set_xlabel('Second-order welfare change (percent)')
    ax.set_title(f'Distributional incidence: {scenario.name}')
    fig.tight_layout()
    write_fig(fig, str(Path(output_dir) / 'figs' / 'map_global_welfare.png'))
    plt.close(fig)


# ---------------------------------------------------------------------------
# Utils
# ---------------------------------------------------------------------------


def _load_json(path: str) -> Dict:
    with open(path, 'r', encoding='utf-8') as fh:
        return json.load(fh)


def _load_yaml(path: str) -> Dict:
    with open(path, 'r', encoding='utf-8') as fh:
        return yaml.safe_load(fh)
