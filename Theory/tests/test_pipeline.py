
from src.empirics.pipeline import (
    StaggeredConfig,
    synthetic_budget_data,
    synthetic_iv_dataset,
    synthetic_staggered_panel,
)


def test_staggered_panel_shapes():
    cfg = StaggeredConfig(units=12, periods=8, early_adopt=3, late_adopt=5, effect=0.7, seed=42)
    panel = synthetic_staggered_panel(cfg)
    assert panel.shape[0] == cfg.units * cfg.periods
    assert {'i', 't', 'D', 'y', 'adoption'}.issubset(panel.columns)
    assert panel['D'].max() <= 1.0


def test_synthetic_iv_strength():
    strong = synthetic_iv_dataset(n=200, strength=0.8, seed=0)
    weak = synthetic_iv_dataset(n=200, strength=0.05, seed=0)
    assert strong['Z'].shape == (200, 2)
    assert strong['cluster'].shape[0] == 200
    assert strong['x'].var() > weak['x'].var()


def test_budget_dataset():
    df = synthetic_budget_data(seed=3)
    assert not df.empty
    assert {'group', 'household', 'good', 'income', 'price', 'expenditure'}.issubset(df.columns)
    assert df['expenditure'].min() >= 0.0
