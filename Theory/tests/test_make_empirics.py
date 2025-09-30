from pathlib import Path

from sims.make_empirics import (
    generate_event_study_outputs,
    generate_iv_outputs,
)
from src.empirics.pipeline import StaggeredConfig


def test_event_study_outputs(tmp_path):
    cfg = StaggeredConfig(units=12, periods=8, effect=0.8, seed=3)
    table, pretrend = generate_event_study_outputs(tmp_path, cfg)

    assert not table.empty
    assert 'ci_low' in table.columns
    assert (tmp_path / 'tables' / 'es_main.tex').exists()
    assert (tmp_path / 'tables' / 'es_pretrend.tex').exists()
    assert (tmp_path / 'figs' / 'event_study.png').exists()
    assert pretrend['value'].iloc[0] >= 0.0


def test_iv_outputs(tmp_path):
    iv_table = generate_iv_outputs(tmp_path, n=160, seed=5)

    assert set(iv_table['scenario']) == {'Strong', 'Weak'}
    assert (tmp_path / 'tables' / 'iv_main.tex').exists()
    assert (tmp_path / 'figs' / 'iv_diagnostics.png').exists()
    assert iv_table['F_first'].max() > iv_table['F_first'].min()
