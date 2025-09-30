import sys

import numpy as np
import sims.make_distributional as dist
from src.empirics.engel import estimate_sg_from_budgets
from src.empirics.pipeline import synthetic_budget_data


def test_estimate_sg_from_synthetic_data():
    df = synthetic_budget_data(groups=("Low", "High"), sectors=5, seed=1)
    alpha, gamma = estimate_sg_from_budgets(df)
    for group in alpha:
        assert np.isclose(alpha[group].sum(), 1.0, atol=1e-6)
        assert np.all(alpha[group] >= 0)
        assert np.all(gamma[group] >= 0)


def test_make_distributional_outputs(tmp_path, monkeypatch):
    budget_df = synthetic_budget_data(seed=3)
    data_path = tmp_path / "budgets.csv"
    budget_df.to_csv(data_path, index=False)

    argv = [
        "make_distributional",
        "--budget-data",
        str(data_path),
        "--output-dir",
        str(tmp_path / "tables"),
        "--fig-dir",
        str(tmp_path / "figs"),
        "--cache-dir",
        str(tmp_path / "cache"),
        "--bootstrap",
        "20",
        "--seed",
        "1",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    dist.main()

    table_path = tmp_path / "tables" / "stone_geary_estimates.tex"
    assert table_path.exists()
    table_tex = table_path.read_text()
    assert "alpha\\_se" in table_tex
    assert "gamma\\_se" in table_tex
    assert (tmp_path / "figs" / "stone_geary_engel.png").exists()
    assert (tmp_path / "cache" / "stone_geary_bootstrap.npz").exists()
