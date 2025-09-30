from pathlib import Path

import json
import numpy as np
import yaml

from src.policy.simulate import run_policy_scenarios


def test_policy_pipeline(tmp_path):
    cache_dir = tmp_path / 'cache'
    cache_dir.mkdir(parents=True, exist_ok=True)
    n_draws, n_groups, n_goods = 4, 3, 10
    goods = np.array([f'sector_{i+1}' for i in range(n_goods)])
    groups = np.array(['Low', 'Middle', 'High'])

    base_alpha = np.linspace(0.05, 0.15, n_goods)
    alpha_draws = []
    gamma_draws = []
    for draw in range(n_draws):
        scale = 1.0 + 0.02 * draw
        alpha_draws.append(np.tile(base_alpha * scale, (n_groups, 1)))
        gamma_draws.append(np.tile(np.linspace(1.0, 2.0, n_goods) * scale, (n_groups, 1)))
    alpha_draws = np.stack(alpha_draws, axis=0)
    gamma_draws = np.stack(gamma_draws, axis=0)

    bootstrap_path = cache_dir / 'stone_geary_bootstrap.npz'
    np.savez(
        bootstrap_path,
        groups=groups,
        goods=goods,
        alpha_draws=alpha_draws,
        gamma_draws=gamma_draws,
    )

    calib_src = Path('data') / 'calibration.yaml'
    calib_data = yaml.safe_load(calib_src.read_text())
    calib_data.setdefault('metadata', {})['stone_geary_bootstrap'] = str(bootstrap_path)
    calib_path = tmp_path / 'calibration.yaml'
    calib_path.write_text(yaml.safe_dump(calib_data))

    policy_config = tmp_path / 'policy.json'
    policy_payload = {
        "scenarios": [
            {"name": "Baseline", "description": "", "policies": {}},
            {
                "name": "Tariff Shock",
                "description": "Synthetic tariff",
                "policies": {
                    "tariffs": [
                        {"origin": "country_1", "dest": "country_2", "sector": "sector_3", "tau": 0.05}
                    ]
                },
            },
        ]
    }
    policy_config.write_text(json.dumps(policy_payload))

    mrio_config = tmp_path / 'mrio.yaml'
    mrio_payload = {
        "mrio": {"source": "SYNTH", "year": 2018, "path": "data/"}
    }
    mrio_config.write_text(yaml.safe_dump(mrio_payload))

    results = run_policy_scenarios(
        str(policy_config),
        output_dir=str(tmp_path),
        calibration_path=str(calib_path),
        mrio_config_path=str(mrio_config),
    )
    assert results
    assert abs(results[0].fo_global) < 1e-9
    assert abs(results[0].so_global) < 1e-9

    world_table = tmp_path / 'tables' / 'world_welfare.tex'
    dist_table = tmp_path / 'tables' / 'distributional_incidence.tex'
    assert world_table.exists()
    assert dist_table.exists()
    dist_tex = dist_table.read_text()
    assert 'ev_ratio' in dist_tex
    assert 'ev_se' in dist_tex
    assert 'ev_p05' in dist_tex

    scenario_fig = tmp_path / 'figs' / 'policy_scenarios.png'
    map_fig = tmp_path / 'figs' / 'map_global_welfare.png'
    assert scenario_fig.exists()
    assert map_fig.exists()

    low_metrics = results[0].ev_groups['Low']
    assert 'ev_ratio' in low_metrics
    assert 'ev_se' in low_metrics
    assert low_metrics['ev_ratio'] > 0
