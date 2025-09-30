
import numpy as np

from src.trade.calibration import load_calibration, calibration_table, stone_geary_matrix


def test_load_calibration_defaults():
    cfg = load_calibration('data/calibration.yaml')
    assert cfg.theta_for('sector_3') == 4.5
    assert cfg.theta_for('unknown_sector') == 5.0
    assert cfg.sigma_for('sector_5') == 1.1
    assert cfg.epsilon_for('sector_2') == 1.5

    table = calibration_table(cfg, ['sector_1', 'sector_3'])
    assert set(table.columns) == {'sector', 'theta_armington', 'sigma_ces', 'epsilon_network'}
    assert len(table) == 2

    sg = stone_geary_matrix(cfg)
    assert not sg.empty
    first = sg.iloc[0]
    assert isinstance(first['alpha'], np.ndarray)
    assert isinstance(first['gamma'], np.ndarray)
